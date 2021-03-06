import os
import random
import logging

from discord.ext import commands, tasks
from dotenv import load_dotenv

from utils.url_builder import build_url_kwargs
from utils.http_helpers import handle_status_code
from utils.http_helpers import send_get_request

log = logging.getLogger(__name__)

load_dotenv()
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
YOUTUBE_SEARCH_LIMIT_PER_HOUR = 4


class YouTube(commands.Cog):
    """
    Main YouTube cog Class
    """
    def __init__(self, bot):
        self.bot = bot
        self.videos = []
        # init to max so we don't run on start up
        self.queries_this_hour = YOUTUBE_SEARCH_LIMIT_PER_HOUR
        self.videos_url = 'https://youtube.googleapis.com/youtube/v3/search'
        self.db_youtube = self.bot.db_client.get_database('YouTube')
        self.db_links_table = self.db_youtube.YoutubeLinks
        log.info('Loading YouTube cog')
        self.populate_on_ready_from_db()
        self.reset_count.start()

    async def request_new_videos(self):
        """
        Requests new videos from the YouTube database and stores them
        It stores them in the local list and the MongoDB database
        The bot is rate limited because Google is really anal with their limits
        :return:
        """
        random_query_word = self.bot.random_words.get_random_query_strict()
        print(random_query_word)
        headers = {
            'Accept': 'application/json'
        }
        query_url = build_url_kwargs(self.videos_url, key=YOUTUBE_API_KEY, q=random_query_word, maxResults='50',
                                     type='video', part='id', safeSearch='strict')
        response = send_get_request(query_url, headers=headers)
        status_code = handle_status_code(response)
        if status_code == 'OK':
            try:
                for item in response.json()['items']:
                    new_link = {'Link': 'https://www.youtube.com/watch?v=' + item['id']['videoId'],
                                'Query': random_query_word}
                    self.videos.append(new_link)
                    self.db_links_table.insert_one(new_link)
            except KeyError:
                pass
        else:
            log.warning('Received response code: ' + str(status_code))
        self.queries_this_hour += 1

    def cog_unload(self):
        self.reset_count.cancel()

    def populate_on_ready_from_db(self):
        """
        Loads in videos from MongoDB
        :return:
        """
        self.videos = [link for link in self.db_links_table.find()]

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

    @commands.command(name="youtube", description="Get a link to a random youtube video", aliases=["ytube", "yt"],
                      brief="Get a random youtube video")
    async def youtube(self, ctx):
        """
        Gets a random YouTube link and returns it to the author
        """
        if self.queries_this_hour < YOUTUBE_SEARCH_LIMIT_PER_HOUR:
            await self.request_new_videos()

        author = ctx.author.mention
        video = random.choice(self.videos)
        await ctx.send(author + ' Check this out on YouTube: '
                       + str(video['Link']))


def setup(bot):
    bot.add_cog(YouTube(bot))
