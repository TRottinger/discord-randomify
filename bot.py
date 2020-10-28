import os

from discord.ext import commands
from dotenv import load_dotenv
import logging

logging.basicConfig(filename='info.log', filemode='w', level=logging.INFO)
log = logging.getLogger(__name__)

# Load twitch client id and secret into file
load_dotenv()
CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')
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
        super().run(TOKEN, reconnect=True)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(ctx.author.mention + '- Sorry, that command does not exist!')


if __name__ == '__main__':
    bot = Bot('!rt ')

