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
TESTING = os.getenv('testing')

if TESTING == 'True':
    TOKEN = os.getenv('TEST_DISCORD_TOKEN')
else:
    TOKEN = os.getenv('DISCORD_TOKEN')

MONGO_DB_URL = os.getenv('MONGO_DB')

OWNER_ID = 179780915558481929
SHARED_SERVER = 773783340763316224


def _guild_prefix(discord_bot, discord_msg):
    guild = discord_msg.guild
    if guild is None:
        return discord_bot.default_prefix
    else:
        # Return both default and custom defined prefix. Makes sure default always works
        custom_prefix = discord_bot.get_guild_prefix(guild.id)
        return [discord_bot.default_prefix, custom_prefix]


def setup_extensions(discord_bot):
    discord_bot.load_extension('cogs.config')
    discord_bot.load_extension('cogs.misc')
    discord_bot.load_extension('cogs.twitch')
    discord_bot.load_extension('cogs.reddit')
    discord_bot.load_extension('cogs.wiki')
    discord_bot.load_extension('cogs.common_randomizers')
    discord_bot.load_extension('cogs.league_of_legends')
    discord_bot.load_extension('cogs.youtube')
    # discord_bot.load_extension('cogs.anime')
    discord_bot.load_extension('cogs.admin')


class Bot(commands.AutoShardedBot):
    def __init__(self, **options):
        super().__init__(command_prefix=_guild_prefix, **options)
        self.db_client = pymongo.MongoClient(MONGO_DB_URL)
        self.db_bot = self.db_client.get_database('Bot')
        self.db_prefix_table = self.db_bot.get_collection('GuildPrefixes')
        self.default_prefix = '!rt '
        self.repeat_dict = {}
        self.owner_id = OWNER_ID
        self.support_id = SHARED_SERVER
        self.help_command = discord.ext.commands.DefaultHelpCommand(dm_help=True)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(ctx.author.mention + '- Sorry, that command does not exist!')

    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.playing,
                                                             name='on the Cloud. !rt help'))

    async def on_guild_join(self, guild):
        channel = self.get_guild(self.support_id).text_channels[0]
        await channel.send('GUILD ADDED ALERT: ' + str(guild) + '. Large guild?: ' + str(guild.large))

    async def on_guild_remove(self, guild):
        channel = self.get_guild(self.support_id).text_channels[0]
        await channel.send('GUILD REMOVED ALERT: ' + str(guild) + '. Large guild?: ' + str(guild.large))

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
    bot = Bot(intents=discord.Intents.default())
    setup_extensions(bot)
    bot.run(TOKEN, reconnect=True)
