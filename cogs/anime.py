
import logging
import random

import discord
from discord.ext import commands, tasks
import mal

from utils.common_utils import get_random_query

log = logging.getLogger(__name__)


class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="anime", description="Get a random anime", brief="Get a random anime. SFW")
    async def anime(self, ctx):
        """
        Queries the MAL api with a random word to get an anime
        """
        query_word = get_random_query()
        # exclude NFSW categories
        query = query_word + '&gx=1&genre%5B%5D=9&genre%5B%5D=12&genre%5B%5D=33&genre%5B%5D=34'
        search = mal.AnimeSearch(query)
        if len(search.results) == 0:
            await ctx.send('I had trouble querying MAL')
        else:
            embed = discord.Embed(title='Random Anime')
            choice = random.choice(search.results)
            embed.add_field(name='Title', value=str(choice.title), inline=True)
            embed.add_field(name='Score', value=str(choice.score), inline=True)
            embed.add_field(name='Synopsis', value=str(choice.synopsis), inline=False)
            embed.add_field(name='Link', value=choice.url, inline=False)
            embed.colour = discord.Colour.dark_magenta()
            await ctx.send(embed=embed)

    @commands.command(name="manga", description="Get a random manga", brief="Get a random manga. SFW")
    async def manga(self, ctx):
        """
        Queries the MAL api with a random word to get an anime
        """
        query_word = get_random_query()
        # exclude NFSW categories
        query = query_word + '&gx=1&genre%5B%5D=9&genre%5B%5D=12&genre%5B%5D=33&genre%5B%5D=34'
        search = mal.MangaSearch(query)
        if len(search.results) == 0:
            await ctx.send('I had trouble querying MAL')
        else:
            embed = discord.Embed(title='Random Manga')
            choice = random.choice(search.results)
            embed.add_field(name='Title', value=str(choice.title), inline=True)
            embed.add_field(name='Score', value=str(choice.score), inline=True)
            embed.add_field(name='Synopsis', value=str(choice.synopsis), inline=False)
            embed.add_field(name='Link', value=choice.url, inline=False)
            embed.colour = discord.Colour.dark_magenta()
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Anime(bot))
