import os
import random

import requests
from discord.ext import commands, tasks
from dotenv import load_dotenv

from utils.common_utils import get_random_query
from utils.url_builder import build_url

load_dotenv()
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
YOUTUBE_SEARCH_LIMIT_PER_HOUR = 5


class YouTube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.videos = []
        self.frequency = 0

    @tasks.loop(minutes=60)
    async def reset_count(self):
        self.frequency = 0

    @commands.command(name="youtube", description="Get a link to a random youtube video", aliases=["ytube", "yt"],
                      brief="Get a random youtube video")
    async def youtube(self, ctx):

        if self.frequency < YOUTUBE_SEARCH_LIMIT_PER_HOUR:
            random_query_word = get_random_query()
            print(random_query_word)
            headers = {
                'Accept': 'application/json'
            }
            videos_url = 'https://youtube.googleapis.com/youtube/v3/search'
            query_url = build_url(videos_url, "key=" + YOUTUBE_API_KEY, "q=" + random_query_word, "maxResults=50",
                                  "type=video", "part=id")
            print(query_url)
            response = requests.get(query_url, headers=headers)
            print(response.json())
            for item in response.json()['items']:
                print(item['id'])
                self.videos.append(item['id']['videoId'])
            self.frequency += 1

        author = ctx.author.mention
        print(self.videos)
        await ctx.send(author + ' Check this out on YouTube: https://www.youtube.com/watch?v='
                       + random.choice(self.videos))


def setup(bot):
    bot.add_cog(YouTube(bot))
