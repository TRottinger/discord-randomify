
import logging
import random

import discord
from discord.ext import commands, tasks
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

    @commands.command(name="anime", description="Get a random anime", brief="Get a random anime. SFW")
    async def anime(self, ctx):
        """
        Queries the MAL api with a random word to get an anime
        """
        query_word = self.bot.random_words.get_random_query()
        # exclude NFSW categories
        query = query_word + '&gx=1&genre%5B%5D=9&genre%5B%5D=12&genre%5B%5D=33&genre%5B%5D=34'
        search = mal.AnimeSearch(query)

        # Try again with a stricter word
        if len(search.results == 0):
            query = query.replace(query_word, self.bot.random_words.get_random_query_strict)
            search = mal.AnimeSearch(query)

        if len(search.results) == 0:
            await ctx.send('I could not find an anime with the given parameters')
        else:
            embed = discord.Embed(title='Random Anime')
            choice = random.choice(search.results)
            output_embed = await populate_embed(choice, embed)
            await ctx.send(embed=output_embed)

    @commands.command(name="manga", description="Get a random manga", brief="Get a random manga. SFW")
    async def manga(self, ctx):
        """
        Queries the MAL api with a random word to get a manga
        """
        query_word = self.bot.random_words.get_random_query()
        # exclude NFSW categories
        query = query_word + '&gx=1&genre%5B%5D=9&genre%5B%5D=12&genre%5B%5D=33&genre%5B%5D=34'
        search = mal.MangaSearch(query)

        # Try again with a stricter word
        if len(search.results == 0):
            query = query.replace(query_word, self.bot.random_words.get_random_query_strict)
            search = mal.MangaSearch(query)

        if len(search.results) == 0:
            await ctx.send('I could not find a manga with the given parameters')
        else:
            embed = discord.Embed(title='Random Manga')
            choice = random.choice(search.results)
            output_embed = await populate_embed(choice, embed)
            await ctx.send(embed=output_embed)


def setup(bot):
    bot.add_cog(Anime(bot))
