#!/usr/bin/python3
import os
from discord.ext import commands
from dotenv import load_dotenv
import pymongo

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


class Bot(commands.AutoShardedBot):
    """
    The main Bot class for Randomify
    """

    def __init__(self, **options):
        super().__init__(**options)
        self.db_client: pymongo.MongoClient = pymongo.MongoClient(MONGO_DB_URL)
        self.db_bot = self.db_client.get_database('Bot')
        self.db_prefix_table = self.db_bot.get_collection('GuildPrefixes')
        self.default_prefix = '!rt '
        self.repeat_dict = {}
        self.support_id = SHARED_SERVER
        self.help_command = CustomHelpCommand()
        self.random_words = RandomQuery()

    def setup_extensions(self):
        """
        Loads the extensions for the bot
        :return:
        """
        self.load_extension('cogs.config')
        self.load_extension('cogs.misc')
        self.load_extension('cogs.twitch')
        self.load_extension('cogs.reddit')
        self.load_extension('cogs.wiki')
        self.load_extension('cogs.common_randomizers')
        self.load_extension('cogs.games')
        self.load_extension('cogs.youtube')
        self.load_extension('cogs.anime')
        self.load_extension('cogs.spotify')
        self.load_extension('cogs.topgg')
        self.load_extension('cogs.hollywood')

    def startup(self):
        self.run(TOKEN, reconnect=True)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(ctx.author.mention + ' - Sorry, that command does not exist!')
        elif isinstance(error, commands.CommandOnCooldown):
            string = """Sorry, that command is on cooldown.  You can call this command {times} times every {second} sec
            Try running the command again is {retry} seconds.""".format(
                times=error.cooldown.rate, second=error.cooldown.per, retry=int(error.retry_after))

            await ctx.send(ctx.author.mention + ' ' + string)
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(ctx.author.mention + ', you do not have permissions to run ' + str(ctx.command))

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
        if prefix == '':
            res = False
        elif prefix.isspace():
            res = False
        else:
            entry = {
                'Guild': guild,
                'Prefix': prefix
            }
            self.db_prefix_table.find_one_and_update({'Guild': guild}, {"$set": entry}, upsert=True)
            res = True
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
