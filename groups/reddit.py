import os
import random

import discord
from discord import app_commands
from urllib.request import Request
import urllib.error
import discord

import logging

import asyncpraw
from dotenv import load_dotenv

log = logging.getLogger(__name__)


class Reddit(app_commands.Group):
    def __init__(self):
        super().__init__()
        load_dotenv()
        self.client_id = os.getenv('REDDIT_CLIENT_ID')
        self.client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        self.user_agent = "discord:randomify:v1.1.1 (by /u/" + os.getenv('REDDIT_USERNAME') + ")"
        self.reddit = asyncpraw.Reddit(client_id=self.client_id, client_secret=self.client_secret,
                                       user_agent=self.user_agent)
        self.subreddit_cache = []

    @app_commands.command(name="reddit", description="Get a link to a random subreddit")
    async def reddit(self, interaction: discord.Interaction):
        subreddit = await self.reddit.random_subreddit(nsfw=False)
        if subreddit is None:
            subreddit = random.choice(self.subreddit_cache)
        else:
            self.subreddit_cache.append(subreddit)
        embed = discord.Embed(title='Random Subreddit')
        if subreddit.display_name is not None:
            embed.add_field(name='Name', value=str(subreddit.display_name), inline=False)
        if subreddit.public_description is not None:
            embed.add_field(name='Description', value=str(subreddit.public_description), inline=False)
        if subreddit.subscribers is not None:
            embed.add_field(name='Subscribers', value=str(subreddit.subscribers), inline=False)
        if subreddit.over18 is not None:
            embed.add_field(name='NSFW', value=str(subreddit.over18), inline=False)
        if subreddit.display_name is not None:
            embed.add_field(name='Link', value="http://www.reddit.com/r/" + str(subreddit.display_name), inline=False)
        await interaction.response.send_message(embed=embed)

