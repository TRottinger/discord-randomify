import os

import discord
from dotenv import load_dotenv

from bot import Bot

import logging

from groups.admin import Admin
from groups.twitch import Twitch

load_dotenv()
TESTING = os.getenv('testing')


logging.basicConfig(filename='info.log', filemode='w', level=logging.INFO)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
log = logging.getLogger(__name__)



def startup():
    log.info("Starting Bot")
    owner_id = 179780915558481929
    bot = Bot(intents=discord.Intents.default(),
              activity=discord.Activity(type=discord.ActivityType.playing, name='Using Slash Commands!'),
              owner_id=owner_id)

    log.info("Running bot")
    bot.startup()


if __name__ == '__main__':
    startup()
