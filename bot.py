#!/usr/bin/python3
import os

import discord
from discord.ext import commands
from discord import Activity, ActivityType
from dotenv import load_dotenv
import logging
import dns
import pymongo

logging.basicConfig(filename='info.log', filemode='w', level=logging.INFO)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
log = logging.getLogger(__name__)

# Load twitch client id and secret into file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
MONGO_DB_URL = os.getenv('MONGO_DB')


def _guild_prefix(discord_bot, discord_msg):
    guild = discord_msg.guild
    if guild is None:
        return discord_bot.default_prefix
    else:
        # Return both default and custom defined prefix. Makes sure default always works
        custom_prefix = discord_bot.get_guild_prefix(guild.id)
        return [discord_bot.default_prefix, custom_prefix]


class Bot(commands.AutoShardedBot):
    def __init__(self, **options):
        super().__init__(command_prefix=_guild_prefix, **options)
        self.db_client = pymongo.MongoClient(MONGO_DB_URL)
        self.db_bot = self.db_client.get_database('Bot')
        self.db_prefix_table = self.db_bot.get_collection('GuildPrefixes')
        # map ctx to user to be able to repeat command
        self.default_prefix = '!rt '
        self.repeat_dict = {}
        self.load_extension('cogs.config')
        self.load_extension('cogs.misc')
        self.load_extension('cogs.twitch')
        self.load_extension('cogs.reddit')
        self.load_extension('cogs.wiki')
        self.load_extension('cogs.common_randomizers')
        self.load_extension('cogs.league_of_legends')
        self.load_extension('cogs.youtube')
        # self.load_extension('cogs.anime')
        self.load_extension('cogs.admin')
        super().run(TOKEN, reconnect=True)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(ctx.author.mention + '- Sorry, that command does not exist!')

    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.playing,
                                                             name='on the Cloud. !rt help'))

    async def on_command_completion(self, ctx):
        # add to repeat dict if not 'repeat' called
        str_command = str(ctx.command)
        if str_command != 'repeat':
            self.repeat_dict[str(ctx.message.author)] = ctx

    async def set_guild_prefix(self, guild, prefix):
        res = ''
        if prefix == '':
            res = 'Empty prefix'
        elif prefix.isspace():
            res = 'Badly formed prefix'
        else:
            entry = {
                'Guild': guild,
                'Prefix': prefix
            }
            self.db_prefix_table.find_one_and_update({'Guild': guild}, {"$set": entry}, upsert=True)
            res = ''
        return res

    def get_guild_prefix(self, guild):
        entry = self.db_prefix_table.find_one({'Guild': guild})

        if entry is None:
            prefix = self.default_prefix
        else:
            prefix = str(entry['Prefix'])
        return prefix

    async def get_guilds(self):
        return self.guilds


if __name__ == '__main__':
    bot = Bot()
