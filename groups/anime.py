from urllib.request import Request
import urllib.error

from expiringdict import ExpiringDict
import logging
import random

import discord
from discord import app_commands
from discord.ext import tasks
from mal import *

from utils import http_helpers
from utils.common_utils import RandomQuery

log = logging.getLogger(__name__)

WAIFU_REQUESTS_PER_MINUTE = 30


async def populate_embed(choice, embed):
    embed.add_field(name='Title', value=str(choice.title), inline=True)
    embed.add_field(name='Score', value=str(choice.score), inline=True)
    embed.add_field(name='Synopsis', value=str(choice.synopsis), inline=False)
    embed.add_field(name='Link', value=choice.url, inline=False)
    embed.colour = discord.Colour.dark_magenta()
    return embed


class Anime(app_commands.Group):
    def __init__(self, random_words: RandomQuery):
        super().__init__()
        log.info('Loading Anime cog')
        self.random_words = random_words
        self.anime_cache = ExpiringDict(max_len=5000, max_age_seconds=900)
        self.manga_cache = ExpiringDict(max_len=5000, max_age_seconds=900)
        self.waifu_cache = ExpiringDict(max_len=5000, max_age_seconds=60*60*24)
        self.waifu_limit = 0
        self.reset_waifu_count.start()

    @tasks.loop(seconds=60)
    async def reset_waifu_count(self):
        """
        Resets the manually set rate limit every minute
        :return:
        """
        self.waifu_limit = 0

    async def cache_anime(self, items):
        for item in items:
            self.anime_cache[item.mal_id] = item

    async def cache_manga(self, items):
        for item in items:
            self.manga_cache[item.mal_id] = item

    @app_commands.command(name="anime", description="Get a random anime")
    async def anime(self, interaction: discord.Interaction):
        """
        Queries the MAL api with a random word to get an anime
        """
        query_word = self.random_words.get_random_query_strict()
        # exclude NFSW categories
        query = query_word + '&genre_ex%5B%5D=9&genre_ex%5B%5D=49&genre_ex%5B%5D=12'
        try:
            search = AnimeSearch(query)
        except Exception as e:
            log.warning('Trouble querying anime')
            log.warning(str(e))
            await interaction.response.send_message('I had trouble processing the request')
            return

        if len(search.results) == 0:
            if len(self.anime_cache) > 0:
                choice = random.choice(list(self.anime_cache.values()))
            else:
                log.info('Setting to None')
                choice = None
        else:
            choice = random.choice(search.results)

        if choice is None:
            await interaction.response.send_message('I had trouble processing the request')
        else:
            embed = discord.Embed(title='Random Anime')
            log.info('Choice found: ' + str(choice.title))
            await self.cache_anime(search.results)
            output_embed = await populate_embed(choice, embed)
            await interaction.response.send_message(embed=output_embed)

    @app_commands.command(name="manga", description="Get a random manga")
    async def manga(self, interaction: discord.Interaction):
        """
        Queries the MAL api with a random word to get a manga
        """
        query_word = self.random_words.get_random_query_strict()
        # exclude NFSW categories
        query = query_word + '&genre_ex%5B%5D=9&genre_ex%5B%5D=49&genre_ex%5B%5D=12'
        try:
            search = MangaSearch(query)
        except Exception as e:
            log.warning('Trouble querying manga')
            log.warning(str(e))
            await interaction.response.send_message('I had trouble processing the request')
            return

        if len(search.results) == 0:
            if len(self.manga_cache) > 0:
                choice = random.choice(list(self.manga_cache.values()))
            else:
                choice = None
        else:
            choice = random.choice(search.results)

        if choice is None:
            await interaction.response.send_message('I had trouble processing the request')
        else:
            embed = discord.Embed(title='Random Manga')
            log.info('Choice found: ' + str(choice.title))
            await self.cache_manga(search.results)
            output_embed = await populate_embed(choice, embed)
            await interaction.response.send_message(embed=output_embed)

    @app_commands.command(name="waifu", description="Get a random waifu")
    async def waifu(self, interaction: discord.Interaction):
        url = "https://mywaifulist.moe/random"
        if self.waifu_limit < WAIFU_REQUESTS_PER_MINUTE:
            try:
                urlopen = urllib.request.Request(url)
                urlopen.add_header('User-Agent', 'Discord-Randomify/v1.1.2')
                if urlopen.full_url.startswith('https'):
                    with urllib.request.urlopen(urlopen) as response:
                        result = str(response.url)
                        name = result.split('/')
                        name = name[len(name)-1]
                        self.waifu_cache[name] = result
            except urllib.error.HTTPError:
                result = 'I\'m being rate limited, so manually click this: ' + url
        else:
            if len(self.waifu_cache) > 0:
                result = random.choice(list(self.waifu_cache.values()))
            else:
                result = 'I\'m being rate limited, so manually click this: ' + url
        await interaction.response.send_message(interaction.user.mention + ' ' + result + '')
