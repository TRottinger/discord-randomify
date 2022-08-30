from code import interact
import os
import random

import discord
from discord import app_commands
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


class Hollywood(app_commands.Group):
    """
    Cog for TV / Movie / etc related functionality
    """
    def __init__(self, random_words):
        super().__init__()
        self.random_words = random_words
        load_dotenv()
        self.tmdb_api_key = os.getenv('TMDB_API_KEY')
        tmdb.API_KEY = self.tmdb_api_key

    def common_query(self, search_type):
        found = False
        response = {}
        attempts = 0
        # try three times to get a result
        while found is False and attempts <= 3:
            search = tmdb.Search()
            if search_type == 'movie':
                query = self.random_words.get_random_query_strict()
                response = search.movie(query=query, include_adult=False, language='en_US')
            elif search_type == 'tv':
                query = self.random_words.get_random_query_strict()
                response = search.tv(query=query, include_adult=False, language='en_US')
            elif search_type == 'person':
                query = self.random_words.get_random_first_name()
                response = search.person(query=query, include_adult=False, language='en_US')
            else:
                query = self.random_words.get_random_query_strict()
                response = search.movie(query=query, include_adult=False, language='en_US')
            if len(response['results']) > 0:
                found = True
            attempts += 1

        if found:
            return random.choice(response['results'])
        else:
            return None

    def common_discover_genre(self, discover_type, genre_id):
        found = False
        response = {}
        attempts = 0
        # try three times to get a result
        while found is False and attempts <= 3:
            discover = tmdb.Discover()
            page = random.randint(1, 100)
            if discover_type == 'movie':
                response = discover.movie(with_genres=genre_id, page=page, include_adult=False, language='en_US')
            elif discover_type == 'tv':
                response = discover.tv(with_genres=genre_id, page=page, include_adult=False, language='en_US')
            if len(response['results']) > 0:
                found = True
            attempts += 1
        if found:
            return random.choice(response['results'])
        else:
            return None

    @app_commands.command(name="movie", description="Get a random movie")
    async def movie(self, interaction: discord.Interaction):
        movie = self.common_query('movie')
        if movie is not None:
            embed = discord.Embed(title='Random Movie')
            output_embed = await prepare_embed(embed, movie)
            await interaction.response.send_message(embed=output_embed)
        else:
            await interaction.response.send_message('I\'m having trouble querying for movies right now.')

    @app_commands.command(name="tv", description="Get a random tv show")
    async def tv(self, interaction: discord.Interaction):
        tv = self.common_query('tv')
        if tv is not None:
            embed = discord.Embed(title='Random TV Show')
            output_embed = await prepare_embed(embed, tv)
            await interaction.response.send_message(embed=output_embed)
        else:
            await interaction.response.send_message('I\'m having trouble querying for tv shows right now.')

    @app_commands.command(name="mediaperson", description="Get a person involved in movies, TV shows, etc")
    async def mediaperson(self, interaction: discord.Interaction):
        person = self.common_query('person')
        if person is not None:
            embed = discord.Embed(title=person['name'] + ' is known for: ')
            embed.set_author(name=person['name'])
            if 'known_for' in person.keys() and person['known_for'][0] is not None:
                output_embed = await prepare_embed(embed, person['known_for'][0])
            else:
                output_embed = embed
            await interaction.response.send_message(embed=output_embed)
        else:
            await interaction.response.send_message('I\'m having trouble querying for tv shows right now.')

    @app_commands.command(name="moviegenre", description="Get a random movie by genre")
    @app_commands.describe(input_genre="The genre to search for")
    async def moviegenre(self, interaction: discord.Interaction, input_genre: str):
        genre = tmdb.Genres()
        response = genre.movie_list(language='en_US')
        genres = {}
        for genre in response['genres']:
            genres[genre['name'].lower()] = genre['id']
        if input_genre not in genres.keys():
            # Maybe add a wait for user to pick a correct genre? Don't want to get spammed.....
            await interaction.response.send_message('Sorry ' + interaction.user.mention + ' that genre is not available. Please select from the '
                           'following list of genres: ' + ', '.join(genres.keys()))
        else:
            genre_id = genres[input_genre]
            movie = self.common_discover_genre('movie', genre_id)
            if movie is not None:
                embed = discord.Embed(title='Random ' + input_genre + ' movie')
                output_embed = await prepare_embed(embed, movie)
                await interaction.response.send_message(embed=output_embed)
            else:
                await interaction.response.send_message('I\'m having trouble querying for movies right now.')

    @app_commands.command(name="tvgenre", description="Get a random tv show by genre")
    @app_commands.describe(input_genre="The genre to search for")
    async def tvgenre(self, interaction: discord.Interaction, input_genre: str):
        genre = tmdb.Genres()
        response = genre.tv_list(language='en_US')
        genres = {}
        for genre in response['genres']:
            genres[genre['name'].lower()] = genre['id']
        if input_genre not in genres.keys():
            # Maybe add a wait for user to pick a correct genre? Don't want to get spammed.....
            await interaction.response.send_message('Sorry ' + interaction.user.mention + ' that genre is not available. Please select from the '
                           'following list of genres: ' + ', '.join(genres.keys()))
        else:
            genre_id = genres[input_genre]
            tv = self.common_discover_genre('tv', genre_id)
            if tv is not None:
                embed = discord.Embed(title='Random ' + input_genre + ' TV show')
                output_embed = await prepare_embed(embed, tv)
                await interaction.response.send_message(embed=output_embed)
            else:
                await interaction.response.send_message('I\'m having trouble querying for tv shows right now.')

