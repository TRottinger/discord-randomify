import os
import random
import logging

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

from utils.url_builder import build_url_kwargs
from utils.http_helpers import handle_status_code, get_access_token, form_auth_headers
from utils.http_helpers import send_get_request

log = logging.getLogger(__name__)

SPOTIFY_QUERY_RATE_PER_HOUR = 8


# This class is very similar to the YouTube class
# I should look into combining them into a "media" class


class Spotify(commands.Cog):
    """
    Main Spotify cog Class
    """

    def __init__(self, bot):
        self.bot = bot

        log.info('Loading Spotify cog')

        self.songs = []
        #initialize to max so that we don't run it on init
        self.queries_this_hour = SPOTIFY_QUERY_RATE_PER_HOUR
        self.search_url = 'https://api.spotify.com/v1/search'
        self.db_spotify = self.bot.db_client.get_database('Spotify')
        self.db_songs_table = self.db_spotify.SpotifySongs
        load_dotenv()
        self.spotify_client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.spotify_client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.access_token = get_access_token(self.spotify_client_id, self.spotify_client_secret,
                                             'https://accounts.spotify.com/api/token')

        self.populate_on_ready_from_db()
        self.reset_auth_code.start()
        self.reset_count.start()

    async def request_new_songs(self):
        """
        Requests new songs from the Spotify database and stores them
        It stores them in the local list and the MongoDB database
        Rate limited to be safe
        :return:
        """
        random_query_word = self.bot.random_words.get_random_query_strict()
        headers = form_auth_headers(self.spotify_client_id, self.access_token)
        query_url = build_url_kwargs(self.search_url, q=random_query_word, limit='50', type='track')
        response = send_get_request(query_url, headers=headers)
        status_code = handle_status_code(response)
        if status_code == 'OK':
            for track in response.json()['tracks']['items']:
                url = track['external_urls']['spotify']
                item = {
                    'Link': url,
                    'Query': random_query_word
                }
                # only add SFW tracks
                if track['explicit'] is False:
                    self.songs.append(item)
                    self.db_songs_table.insert_one(item)
        else:
            log.warning('Received response code: ' + str(status_code))
        self.queries_this_hour += 1

    def populate_on_ready_from_db(self):
        """
        Loads in videos from MongoDB
        :return:
        """
        self.songs = [link for link in self.db_songs_table.find()]

    def cog_unload(self):
        self.reset_count.cancel()
        self.reset_auth_code.cancel()

    @tasks.loop(minutes=60)
    async def reset_count(self):
        """
        Resets the manually set rate limit every hour
        :return:
        """
        log.info("Preparing to reset query wait for Spotify")
        while self.queries_this_hour < SPOTIFY_QUERY_RATE_PER_HOUR:
            await self.request_new_songs()
        self.queries_this_hour = 0

    # auth code expires every 60 minutes.. so lets refresh it
    @tasks.loop(minutes=55)
    async def reset_auth_code(self):
        log.info("Preparing to refresh access token for Spotify")
        self.access_token = get_access_token(self.spotify_client_id, self.spotify_client_secret,
                                             'https://accounts.spotify.com/api/token')

    @commands.command(name="song", description="Get a link to a random Spotify song", aliases=["spotify"],
                      brief="Get a random Spotify song")
    async def song(self, ctx):
        """
        Gets a random Spotify song link and return it to the user
        """
        if self.queries_this_hour < SPOTIFY_QUERY_RATE_PER_HOUR:
            await self.request_new_songs()

        author = ctx.author.mention
        song = random.choice(self.songs)
        await ctx.send(author + ' Check this out on Spotify: '
                       + str(song['Link']))

    @commands.cooldown(3, 60, commands.BucketType.user)
    @commands.command(name="artist", description="Get a link to a random Spotify artist", brief="Random Spotify artist")
    async def artist(self, ctx):
        """
        Get a random Spotify artist and return it to the user
        """
        query = self.bot.random_words.get_random_query_strict()
        headers = form_auth_headers(self.spotify_client_id, self.access_token)
        query_url = build_url_kwargs(self.search_url, q=query, type='artist', limit='50')
        response = send_get_request(query_url, headers)
        status_code = handle_status_code(response)
        if status_code == 'OK':
            # call search endpoint again to get a random track
            if len(response.json()['artists']) != 0:
                artists = response.json()['artists']['items']
                choice = random.choice(artists)
                embed = discord.Embed(title='Random Artist')
                embed.add_field(name='Artist', value=choice['name'], inline=False)
                embed.add_field(name='Link', value=choice['external_urls']['spotify'], inline=False)
                if len(choice['genres']) > 0:
                    embed.add_field(name='Genre(s)', value=choice['genres'], inline=False)
                embed.add_field(name='Popularity', value=choice['popularity'], inline=True)
                embed.add_field(name='Followers', value=choice['followers']['total'], inline=True)
                embed.colour = discord.Colour.green()
                await ctx.send(embed=embed)
            else:
                log.warning('Had trouble and got no artists back')
                log.warning('Return: ' + str(response.json()))
                await ctx.send('I had trouble finding an artist')
        else:
            log.warning('Had trouble and got status code: ' + str(status_code))
            await ctx.send('I had trouble finding an artist')

    @commands.cooldown(3, 60, commands.BucketType.user)
    @commands.command(name="podcast", description="Get a link to a random Spotify podcast",
                      brief="Random Spotify podcast")
    async def podcast(self, ctx, market='US'):
        """
        Get a random Spotify podcast and return it to the user
        Non-Explicit only
        Pass in a custom market for your country. Please use the correct ISO 3166-1 alpha-2 country code
        """
        query = self.bot.random_words.get_random_query_strict()
        headers = form_auth_headers(self.spotify_client_id, self.access_token)
        query_url = build_url_kwargs(self.search_url, q=query, type='show', market=market)
        response = send_get_request(query_url, headers)
        status_code = handle_status_code(response)
        if status_code == 'OK':
            # call search endpoint again to get a random track
            if len(response.json()['shows']) != 0:
                shows = response.json()['shows']['items']
                good_shows = []
                for show in shows:
                    if show['explicit'] is False:
                        good_shows.append(show)

                choice = random.choice(good_shows)
                if len(good_shows) > 0:
                    embed = discord.Embed(title='Random Podcast')
                    embed.add_field(name='Podcast', value=choice['name'], inline=False)
                    embed.add_field(name='Description', value=choice['description'], inline=False)
                    embed.add_field(name='Episodes', value=choice['total_episodes'], inline=False)
                    embed.add_field(name='Link', value=choice['external_urls']['spotify'], inline=False)
                    embed.colour = discord.Colour.green()
                    await ctx.send(embed=embed)
                else:
                    log.warning('No good shows. Must have gotten a bad word')
                    await ctx.send('I had trouble finding a podcast')
            else:
                log.warning('Had trouble and got no shows back')
                log.warning('Return: ' + str(response.json()))
                await ctx.send('I had trouble finding a podcast')
        else:
            log.warning('Had trouble and got status code: ' + str(status_code))
            await ctx.send('I had trouble finding a podcast')


def setup(bot):
    bot.add_cog(Spotify(bot))
