import os
import random
import logging

from discord.ext import commands, tasks
from dotenv import load_dotenv

from utils.common_utils import get_random_query
from utils.url_builder import build_url_kwargs
from utils.http_helpers import handle_status_code, get_access_token, form_auth_headers
from utils.http_helpers import send_get_request

log = logging.getLogger(__name__)

SPOTIFY_QUERY_RATE_PER_HOUR = 10

# This class is very similar to the YouTube class
# I should look into combining them into a "media" class


class Spotify(commands.Cog):
    """
    Main YouTube cog Class
    """
    def __init__(self, bot):
        self.bot = bot
        self.songs = []
        self.queries_this_hour = 0
        self.songs_url = 'https://api.spotify.com/v1/search'
        self.db_spotify = self.bot.db_client.get_database('Spotify')
        self.db_songs_table = self.db_spotify.SpotifySongs
        load_dotenv()
        self.spotify_client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.spotify_client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.access_token = get_access_token(self.spotify_client_id, self.spotify_client_secret,
                                             'https://accounts.spotify.com/api/token')

    async def request_new_songs(self):
        """
        Requests new songs from the Spotify database and stores them
        It stores them in the local list and the MongoDB database
        Rate limited to be safe
        :return:
        """
        random_query_word = get_random_query()
        print(random_query_word)
        headers = form_auth_headers(self.spotify_client_id, self.access_token)
        query_url = build_url_kwargs(self.songs_url, q=random_query_word, limit='50', type='track')
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

    async def populate_on_ready_from_db(self):
        """
        Loads in videos from MongoDB
        :return:
        """
        self.songs = [link for link in self.db_songs_table.find()]

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Populates from DB on bot start up
        :return:
        """
        log.info('Loading Spotify cog')
        await self.populate_on_ready_from_db()
        await self.reset_count.start()

    @tasks.loop(minutes=60)
    async def reset_count(self):
        """
        Resets the manually set rate limit every hour
        :return:
        """
        self.queries_this_hour = 0

    @reset_count.before_loop
    async def before_reset_count(self):
        """
        Does some stuff before resetting the count. Might as well use our hourly rate if it wasn't met
        :return:
        """
        log.info("Preparing to reset count")
        while self.queries_this_hour < SPOTIFY_QUERY_RATE_PER_HOUR:
            await self.request_new_songs()
        await self.bot.wait_until_ready()

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


def setup(bot):
    bot.add_cog(Spotify(bot))
