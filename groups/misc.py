import logging
import os

import aiohttp
import discord
from discord import app_commands
import random
from dotenv import load_dotenv
from utils import http_helpers

log = logging.getLogger(__name__)


class MiscFunctions(app_commands.Group):
    def __init__(self, loop, random_words):
        super().__init__()
        load_dotenv()
        self.cat_api_key = os.getenv('CAT_API_KEY')
        self.session = aiohttp.ClientSession(loop=loop)
        self.random_words = random_words

    @app_commands.command(name='time', description='Get a random time')
    async def time(self, interaction: discord.Interaction):
        """
        Gets a random time and outputs it to the user. Format is 24 hour clock.
        """
        hour = f'{random.randint(0, 23):02}'
        minute = f'{random.randint(0, 59):02}'
        time = str(hour) + ':' + str(minute)
        await interaction.response.send_message(interaction.user.mention + ' ' + time)

    @app_commands.command(name='emoji', description='Get a random emoji from your server')
    @app_commands.guild_only()
    async def emoji(self, interaction: discord.Interaction):
        """
        Selects a random emoji that the bot has access to and outputs it to the channel
        """
        # emojis = self.bot.emojis
        # emoji_choice = random.choice(emojis)
        # await interaction.response.send_message(str(emoji_choice))

        # Changing to only be from current guild for safety reasons
        emojis = interaction.guild.emojis
        if len(emojis) == 0:
            await interaction.response.send_message('There are no custom emojis for this server')
        else:
            emoji_choice = random.choice(emojis)
            await interaction.response.send_message(str(emoji_choice))

    # @commands.command(name='emojis', description='Get some random emojis this bot has access to',
    #                  brief='Emojis. Defaults to 5')
    # async def emojis(self, interaction: discord.Interaction, *, arg=5):
    #    """
    #    Selects a certain amount of emojis that the bot has access to and outputs them to the channel
    #    The bot will output it in an embedded message
    #    An argument for the number of emojis can be passed in. Default 5. Max 20
    #    Example: emojis 10
    #    :param ctx:
    #    :param arg:
    #    :return:
    #    """
        #if arg > 20:
        #    await interaction.response.send_message(ctx.author.mention + ' too many emojis requested.')
        #else:
        #    emojis = self.bot.emojis
        #    emoji_choices = random.sample(emojis, k=arg)
        #    embed = discord.Embed(title='Emojis')
        #    for emoji in emoji_choices:
        #        embed.add_field(name=str(emoji.name), value=str(emoji))
        #    await interaction.response.send_message(embed=embed)

    @app_commands.command(name='dog', description='Get a random doggo picture!')
    async def dog(self, interaction: discord.Interaction):
        """
        Uses the dog.ceo/dog-api endpoint to get a random doggo!
        """
        response = await http_helpers.send_async_get_request('https://dog.ceo/api/breeds/image/random', headers=None,
                                                             session=self.session)
        print(response)
        if response['status'] == 'success':
            result = response['message']
        else:
            result = 'Sorry, I had trouble finding a dog'
        await interaction.response.send_message(str(result))

    @app_commands.command(name='cat', description='Get a random cat picture!')
    async def cat(self, interaction: discord.Interaction):
        """
        Uses the cataas.com endpoint to get a random cat
        """
        headers = {
            'x-api-key': self.cat_api_key
        }
        response = http_helpers.send_get_request('https://api.thecatapi.com/v1/images/search', headers=headers)
        if http_helpers.handle_status_code(response) == 'OK':
            result = random.choice(response.json())
            result = result['url']
        else:
            result = 'Sorry, I had trouble finding a cat'

        await interaction.response.send_message(str(result))

    @app_commands.command(name='query', description='Get a random query word')
    async def query(self, interaction: discord.Interaction):
        """
        Gets a random query and outputs it
        """
        choice = self.random_words.get_random_query()
        await interaction.response.send_message(interaction.user.mention + ' you got: ' + choice)

