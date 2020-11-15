from expiringdict import ExpiringDict
import logging
import random

import discord
from discord.ext import commands
import mal

log = logging.getLogger(__name__)


async def populate_embed(choice, embed):
    embed.add_field(name='Title', value=str(choice.title), inline=True)
    embed.add_field(name='Score', value=str(choice.score), inline=True)
    embed.add_field(name='Synopsis', value=str(choice.synopsis), inline=False)
    embed.add_field(name='Link', value=choice.url, inline=False)
    embed.colour = discord.Colour.dark_magenta()
    return embed


class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.anime_cache = ExpiringDict(max_len=5000, max_age_seconds=900)
        self.manga_cache = ExpiringDict(max_len=5000, max_age_seconds=900)

    @commands.Cog.listener()
    async def on_ready(self):
        log.info('Loading Anime cog')

    async def cache_anime(self, items):
        for item in items:
            self.anime_cache[item.mal_id] = item

    async def cache_manga(self, items):
        for item in items:
            self.manga_cache[item.mal_id] = item

    @commands.command(name="anime", description="Get a random anime", brief="Get a random anime. SFW")
    async def anime(self, ctx):
        """
        Queries the MAL api with a random word to get an anime
        """
        query_word = self.bot.random_words.get_random_query_strict()
        # exclude NFSW categories
        query = query_word + '&gx=1&genre%5B%5D=9&genre%5B%5D=12&genre%5B%5D=33&genre%5B%5D=34'
        try:
            search = mal.AnimeSearch(query)
        except Exception as e:
            log.warning('Trouble querying anime')
            log.warning(str(e))
            await ctx.send('I had trouble processing the request')
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
            await ctx.send('I had trouble processing the request')
        else:
            embed = discord.Embed(title='Random Anime')
            log.info('Choice found: ' + str(choice.title))
            await self.cache_anime(search.results)
            output_embed = await populate_embed(choice, embed)
            await ctx.send(embed=output_embed)

    @commands.command(name="manga", description="Get a random manga", brief="Get a random manga. SFW")
    async def manga(self, ctx):
        """
        Queries the MAL api with a random word to get a manga
        """
        query_word = self.bot.random_words.get_random_query_strict()
        # exclude NFSW categories
        query = query_word + '&gx=1&genre%5B%5D=9&genre%5B%5D=12&genre%5B%5D=33&genre%5B%5D=34'
        try:
            search = mal.MangaSearch(query)
        except Exception as e:
            log.warning('Trouble querying manga')
            log.warning(str(e))
            await ctx.send('I had trouble processing the request')
            return

        if len(search.results) == 0:
            if len(self.manga_cache) > 0:
                choice = random.choice(list(self.manga_cache.values()))
            else:
                choice = None
        else:
            choice = random.choice(search.results)

        if choice is None:
            await ctx.send('I had trouble processing the request')
        else:
            embed = discord.Embed(title='Random Manga')
            log.info('Choice found: ' + str(choice.title))
            await self.cache_manga(search.results)
            output_embed = await populate_embed(choice, embed)
            await ctx.send(embed=output_embed)


def setup(bot):
    bot.add_cog(Anime(bot))
