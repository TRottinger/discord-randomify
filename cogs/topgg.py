import asyncio
import os

import dbl
import discord
from discord.ext import tasks, commands
from dotenv import load_dotenv

import logging

log = logging.getLogger(__name__)


class TopGG(commands.Cog):
    """
    Class for TopGG API Calls
    """
    def __init__(self, bot):
        self.bot = bot
        load_dotenv()
        self.token = os.getenv('TOPGG_TOKEN')
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True)


    async def on_guild_post(self):
        log.info("Posted server count")

    async def get_if_user_voted(self, user_id):
        try:
            vote = await self.dblpy.get_user_vote(user_id)
            return vote
        except Exception as e:
            log.warning('Exception: ' + str(e))
            return False

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        log.info('Received an upvote: ' + str(data))

    @commands.is_owner()
    @commands.command(hidden=True)
    async def guildcount(self, ctx):
        info = self.dblpy.guild_count()
        await ctx.author.send(str(info))

    @commands.is_owner()
    @commands.command(hidden=True)
    async def upvotes(self, ctx):
        try:
            info = await self.dblpy.get_bot_upvotes()
            print(str(info))
        except Exception as e:
            log.warning('Exception: ' + str(e))


def setup(bot):
    bot.add_cog(TopGG(bot))
