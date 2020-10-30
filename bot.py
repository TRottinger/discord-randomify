import os

import discord
from discord.ext import commands
from discord import Activity, ActivityType
from dotenv import load_dotenv
import logging

logging.basicConfig(filename='info.log', filemode='w', level=logging.INFO)
log = logging.getLogger(__name__)

# Load twitch client id and secret into file
load_dotenv()
CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
TOKEN = os.getenv('DISCORD_TOKEN')

log.info('CLIENT_ID: ' + CLIENT_ID)
log.info('CLIENT_SECRET: ' + CLIENT_SECRET)
log.info('TOKEN: ' + TOKEN)


class Bot(commands.AutoShardedBot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.load_extension('cogs.twitch')
        self.load_extension('cogs.reddit')
        self.load_extension('cogs.wiki')
        self.load_extension('cogs.common_randomizers')
        self.load_extension('cogs.league_of_legends')
        self.load_extension('cogs.youtube')
        super().run(TOKEN, reconnect=True)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(ctx.author.mention + '- Sorry, that command does not exist!')

    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming,
                                                             name='on the Cloud. !rt help'))


if __name__ == '__main__':
    bot = Bot('!rt ')
