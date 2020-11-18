import os
import random

import discord
from discord.ext import commands
import logging

from dotenv import load_dotenv
import tmdbsimple as tmdb

log = logging.getLogger(__name__)

CACHE_MINUTES = 100


async def prepare_embed(embed, item):
    fields = item.keys()
    if 'title' in fields:
        embed.add_field(name='Title', value=item['title'], inline=False)
    elif 'name' in fields:
        embed.add_field(name='Title', value=item['name'], inline=False)
    if 'overview' in fields and item['overview'] != '':
        embed.add_field(name='Overview', value=item['overview'], inline=False)
    if 'release_date' in fields:
        embed.add_field(name='Release Date', value=item['release_date'], inline=True)
    if 'vote_average' in fields:
        embed.add_field(name='Score', value=str(item['vote_average']), inline=True)
    if 'original_language' in fields:
        embed.add_field(name='Language', value=item['original_language'], inline=True)
    if 'poster_path' in fields and item['poster_path'] is not None:
        embed.set_thumbnail(url='https://image.tmdb.org/t/p/w500' + item['poster_path'])
    embed.set_footer(text='Results from TMDB: https://www.themoviedb.org/')
    return embed


class Hollywood(commands.Cog):
    """
    Cog for TV / Movie / etc related functionality
    """
    def __init__(self, bot):
        self.bot = bot
        load_dotenv()
        self.tmdb_api_key = os.getenv('TMDB_API_KEY')
        tmdb.API_KEY = self.tmdb_api_key

    @commands.command(name="movie", description="Get a random movie", brief="Get a random movie",
                      aliases=["mv"])
    async def movie(self, ctx):
        found = False
        response = {}
        attempts = 0
        # try three times to get a result
        while found is False or attempts == 3:
            random_query_word = self.bot.random_words.get_random_query_strict()
            search = tmdb.Search()
            response = search.movie(query=random_query_word, include_adult=False, language='en_US')
            if len(response['results']) > 0:
                found = True
            attempts += 1
        if found:
            choice = random.choice(response['results'])
            embed = discord.Embed(title='Random Movie')
            output_embed = await prepare_embed(embed, choice)
            await ctx.send(embed=output_embed)
        else:
            await ctx.send('I\'m having trouble querying for tv shows right now.')

    @commands.command(name="tv", description="Get a random tv show", brief="Get a random tv show",
                      aliases=["tvshow"])
    async def tv(self, ctx):
        found = False
        response = {}
        attempts = 0
        while found is False or attempts == 3:
            random_query_word = self.bot.random_words.get_random_query_strict()
            search = tmdb.Search()
            response = search.tv(query=random_query_word, include_adult=False, language='en_US')
            if len(response['results']) > 0:
                found = True
            attempts += 1
        if found:
            choice = random.choice(response['results'])
            embed = discord.Embed(title='Random TV Show')
            output_embed = await prepare_embed(embed, choice)
            await ctx.send(embed=output_embed)
        else:
            await ctx.send('I\'m having trouble querying for tv shows right now.')

    @commands.command(name="mediaperson", description="Get a person involved in movies, TV shows, etc",
                      brief="Get a person involved in media", aliases=["media"])
    async def mediaperson(self, ctx):
        found = False
        response = {}
        attempts = 0
        while found is False or attempts == 3:
            random_name = self.bot.random_words.get_random_first_name()
            search = tmdb.Search()
            response = search.person(query=random_name, include_adult=False, language='en_US')
            if len(response['results']) > 0:
                found = True
            attempts += 1
        if found:
            choice = random.choice(response['results'])
            embed = discord.Embed(title=choice['name'] + ' is known for: ')
            embed.set_author(name=choice['name'])
            if 'known_for' in choice.keys() and choice['known_for'][0] is not None:
                output_embed = await prepare_embed(embed, choice['known_for'][0])
            else:
                output_embed = embed
            await ctx.send(embed=output_embed)
        else:
            await ctx.send('I\'m having trouble querying for tv shows right now.')


def setup(bot):
    bot.add_cog(Hollywood(bot))
