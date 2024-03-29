import os
import random
import logging
import pymongo

import discord
from discord import app_commands
from discord.ext import tasks
from dotenv import load_dotenv

from utils.url_builder import build_url_kwargs
from utils.http_helpers import handle_status_code
from utils.http_helpers import send_get_request

log = logging.getLogger(__name__)

load_dotenv()
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
YOUTUBE_SEARCH_LIMIT_PER_HOUR = 4


class Youtube(app_commands.Group):
    """
    Main YouTube cog Class
    """
    def __init__(self, db_client, random_words):
        super().__init__()
        # init to max so we don't run on start up
        self.queries_this_hour = YOUTUBE_SEARCH_LIMIT_PER_HOUR
        self.videos_url = 'https://youtube.googleapis.com/youtube/v3/search'
        self.random_words = random_words
        self.db_youtube = db_client.get_database('YouTube')
        self.db_links_table = self.db_youtube.YoutubeLinks
        log.info('Loading YouTube cog')
        self.reset_count.start()

    async def request_new_videos(self):
        """
        Requests new videos from the YouTube database and stores them
        It stores them in the local list and the MongoDB database
        The bot is rate limited because Google is really anal with their limits
        :return:
        """
        random_query_word = self.random_words.get_random_query_strict()
        headers = {
            'Accept': 'application/json'
        }
        query_url = build_url_kwargs(self.videos_url, key=YOUTUBE_API_KEY, q=random_query_word, maxResults='50',
                                     type='video', part='id', safeSearch='strict')
        response = send_get_request(query_url, headers=headers)
        status_code = handle_status_code(response)

        new_items = []

        if status_code == 'OK':
            try:
                for item in response.json()['items']:
                    new_item = {'Link': 'https://www.youtube.com/watch?v=' + item['id']['videoId'],
                                'Query': random_query_word}
                    new_items.append(new_item)
            except KeyError:
                pass
        else:
            log.warning('Received response code: ' + str(status_code))

        self.db_links_table.insert_many(new_items)
        self.queries_this_hour += 1

    def cog_unload(self):
        self.reset_count.cancel()

    @tasks.loop(minutes=60)
    async def reset_count(self):
        """
        Resets the manually set rate limit every hour
        :return:
        """
        log.info("Preparing to reset count")
        while self.queries_this_hour < YOUTUBE_SEARCH_LIMIT_PER_HOUR:
            await self.request_new_videos()
        self.queries_this_hour = 0

    @app_commands.command(name="video", description="Get a link to a random youtube video")
    async def video(self, interaction: discord.Interaction):
        """
        Gets a random YouTube link and returns it to the author
        """
        if self.queries_this_hour < YOUTUBE_SEARCH_LIMIT_PER_HOUR:
            await self.request_new_videos()

        author = interaction.user.mention
        videoCursor = [video for video in self.db_links_table.aggregate([{ "$sample": { "size": 1 }}])]
        if len(videoCursor) > 0:
            video = videoCursor[0]
            await interaction.response.send_message(author + ' Check this out on YouTube: '
                        + str(video['Link']))
        else:
            await interaction.response.send_message(author + ' sorry :( I had issues with getting you a video.')
