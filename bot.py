#!/usr/bin/python3
import asyncio
import logging
import os
from dotenv import load_dotenv
import pymongo
import discord
from discord import app_commands
from groups.admin import Admin
from groups.hollywood import Hollywood
from groups.misc import MiscFunctions
from groups.reddit import Reddit
from groups.spotify import Spotify
from groups.twitch import Twitch
from groups.anime import Anime
from groups.common_randomizers import CommonRandomizer
from groups.config import Config
from groups.wiki import Wiki
from groups.youtube import Youtube

# Load twitch client id and secret into file
from utils.common_utils import RandomQuery
from utils.help_command import CustomHelpCommand

load_dotenv()
TESTING = os.getenv('testing')

if TESTING == 'True':
    TOKEN = os.getenv('TEST_DISCORD_TOKEN')
else:
    TOKEN = os.getenv('DISCORD_TOKEN')

MONGO_DB_URL = os.getenv('MONGO_DB')

SHARED_SERVER = 773783340763316224

log = logging.getLogger(__name__)

class Bot(discord.Client):
    """
    The main Bot class for Randomify
    """

    def __init__(self, **options):
        super().__init__(**options)
        self.tree = app_commands.CommandTree(self)
        self.db_client: pymongo.MongoClient = pymongo.MongoClient(MONGO_DB_URL)
        self.db_bot = self.db_client.get_database('Bot')
        self.repeat_dict = {}
        self.support_id = SHARED_SERVER
        self.help_command = CustomHelpCommand()
        self.random_words = RandomQuery()

    async def setup_hook(self):
        self.tree.add_command(Admin())
        self.tree.add_command(Anime(self.random_words))
        self.tree.add_command(CommonRandomizer())
        self.tree.add_command(Config())
        self.tree.add_command(Twitch())
        self.tree.add_command(Hollywood(self.random_words))
        self.tree.add_command(MiscFunctions(self.loop, self.random_words))
        self.tree.add_command(Wiki())
        self.tree.add_command(Youtube(self.db_client, self.random_words))
        self.tree.add_command(Reddit())
        self.tree.add_command(Spotify(self.db_client, self.random_words, self.loop))
        self.tree.on_error = self.on_error
        await self.tree.sync()

    def startup(self):
        self.run(TOKEN, reconnect=True)

    async def on_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message(error)

    async def on_guild_join(self, guild):
        channel = self.get_guild(self.support_id).text_channels[0]
        await channel.send('GUILD ADDED ALERT: ' + str(guild) + '. Large guild?: ' + str(guild.large))

    async def on_guild_remove(self, guild):
        channel = self.get_guild(self.support_id).text_channels[0]
        await channel.send('GUILD REMOVED ALERT: ' + str(guild) + '. Large guild?: ' + str(guild.large))

    async def get_guilds(self):
        return self.guilds
