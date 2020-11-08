import discord

from bot import Bot

import logging


logging.basicConfig(filename='info.log', filemode='w', level=logging.INFO)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
log = logging.getLogger(__name__)


def _guild_prefix(discord_bot, discord_msg):
    guild = discord_msg.guild
    if guild is None:
        return discord_bot.default_prefix
    else:
        # Return both default and custom defined prefix. Makes sure default always works
        custom_prefix = discord_bot.get_guild_prefix(guild.id)
        return [discord_bot.default_prefix, custom_prefix]


def startup():
    log.info("Starting Bot")
    owner_id = 179780915558481929
    bot = Bot(intents=discord.Intents.default(),
              activity=discord.Activity(type=discord.ActivityType.playing, name='Random Time! !rt help'),
              owner_id=owner_id,
              command_prefix=_guild_prefix)
    log.info("Loading extensions")
    bot.setup_extensions()
    log.info("Running bot")
    bot.startup()


if __name__ == '__main__':
    startup()
