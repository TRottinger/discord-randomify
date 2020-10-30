import os
import random

import requests
from discord.ext import commands, tasks
from dotenv import load_dotenv

from utils.common_utils import get_random_query
from utils.url_builder import build_url

load_dotenv()
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
YOUTUBE_SEARCH_LIMIT_PER_HOUR = 4


class YouTube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.videos = []
        self.queries_this_hour = 0

    def request_new_videos(self):
        random_query_word = get_random_query()
        print(random_query_word)
        headers = {
            'Accept': 'application/json'
        }
        videos_url = 'https://youtube.googleapis.com/youtube/v3/search'
        query_url = build_url(videos_url, "key=" + YOUTUBE_API_KEY, "q=" + random_query_word, "maxResults=50",
                              "type=video", "part=id")
        response = requests.get(query_url, headers=headers)
        for item in response.json()['items']:
            self.videos.append(item['id']['videoId'])
        self.queries_this_hour += 1

    @commands.Cog.listener()
    async def on_ready(self):
        print('Loading YouTube cog')
        await self.reset_count.start()

    @tasks.loop(minutes=60)
    async def reset_count(self):
        self.queries_this_hour = 0

    @reset_count.before_loop
    async def before_reset_count(self):
        print('Preparing to reset YouTube query frequency')
        while self.queries_this_hour < YOUTUBE_SEARCH_LIMIT_PER_HOUR:
            self.request_new_videos()
        await self.bot.wait_until_ready()

    @commands.command(name="youtube", description="Get a link to a random youtube video", aliases=["ytube", "yt"],
                      brief="Get a random youtube video")
    async def youtube(self, ctx):

        #if self.queries_this_hour < YOUTUBE_SEARCH_LIMIT_PER_HOUR:
        #    self.request_new_videos()
        #
        author = ctx.author.mention
        #await ctx.send(author + ' Check this out on YouTube: https://www.youtube.com/watch?v='
        #               + random.choice(self.videos))
        await ctx.send(author + ' Sorry, YouTube functionality is currently down until the dev figures out Databases')


def setup(bot):
    bot.add_cog(YouTube(bot))
