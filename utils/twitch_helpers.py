import requests
import os
from dotenv import load_dotenv

from utils import http_helpers
from utils.url_builder import build_twitch_streams_url
import random
import logging

log = logging.getLogger(__name__)

load_dotenv()


class Streamer:
    def __init__(self, name=None, viewers=None):
        self.login_name = name
        self.viewers = viewers


class TwitchHelpers:
    """
    Class for common helpers for Twitch functionality
    """
    def __init__(self, client_id=None, client_secret=None):
        if client_id is None:
            self.client_id = os.getenv('TWITCH_CLIENT_ID')
        else:
            self.client_id = client_id
        if client_secret is None:
            self.client_secret = os.getenv('TWITCH_CLIENT_SECRET')
        else:
            self.client_secret = client_secret
        self.access_token = http_helpers.get_access_token(self.client_id, self.client_secret,
                                                          'https://id.twitch.tv/oauth2/token')

    # Returns a dictionary of top 100 twitch games
    def get_twitch_games(self):
        """
        Returns a list of games and their weights
        :return: dictionary of game id to game name, and weighted game ids
        """
        headers = http_helpers.form_auth_headers(self.client_id, self.access_token)
        response = http_helpers.send_get_request('https://api.twitch.tv/helix/games/top?first=100', headers=headers)

        if http_helpers.handle_status_code(response) != 'OK':
            log.warning("Returned http status code: " + response.status_code)
            game_dict, weighted_game_ids = None, None
        else:
            games = response.json()['data']

            game_dict = {}
            weighted_game_ids = []
            weight = 10

            for game in games:
                game_dict[game['id']] = game['name']
                weighted_game_ids.extend([game['id']] * weight)
                if weight != 1:
                    weight -= 1
                    log.info('Weight ' + str(weight))

        return game_dict, weighted_game_ids

    def get_game_by_name(self, game_name):
        """
        returns a game field by game_name
        :param game_name:
        :return: game
        """
        headers = http_helpers.form_auth_headers(self.client_id, self.access_token)
        response = http_helpers.send_get_request('https://api.twitch.tv/helix/games?name=' + game_name,
                                                 headers=headers)
        if http_helpers.handle_status_code(response) != 'OK':
            log.warning("Returned http status code: " + response.status_code)
            log.warning("Returning None")
            game_id = None
        else:
            games = response.json()['data']
            if len(games) > 0:
                log.info('Returning game id: ' + games[0]['id'])
                game_id = games[0]['id']
            else:
                game_id = None

        return game_id

    # Returns a list of streamers
    def get_twitch_streams(self, game_id=0, language=''):
        """
        Gets a list of twitch streams under game_id in the specified language
        :param game_id:
        :param language:
        :return: List of streams
        """
        streams_request_url = 'https://api.twitch.tv/helix/streams'

        headers = http_helpers.form_auth_headers(self.client_id, self.access_token)

        after = '0'
        streamers = []

        # Loop through this function a few times to get a lot of streamers
        # This might have to change if I'm sending too many requests to Twitch.
        for i in range(0, 7):
            request_url = build_twitch_streams_url(streams_request_url, '100', str(game_id), after)

            response = http_helpers.send_get_request(request_url, headers=headers)

            try:
                for data in response.json()['data']:
                    streamers.append(data)
            except KeyError:
                log.warning('No streamers found for game: ' + str(game_id))
                return None

            if str(response.json()['pagination']) == '{}':
                break
            else:
                pag = response.json()['pagination']['cursor']
                after = pag

        return streamers

    def get_streamer(self, game_id):
        """
        Selects a random streamer and returns information about that
        :param game_id:
        :return: streamer
        """
        streamers = self.get_twitch_streams(game_id)

        if streamers is None:
            my_streamer = None
        else:
            streamer = random.choice(streamers)

            streamer_login_name = self.get_streamer_login_name(streamer)
            viewer_count = streamer['viewer_count']

            my_streamer = Streamer(streamer_login_name, viewer_count)
        return my_streamer

    # Returns streamers user name for twitch link
    def get_streamer_login_name(self, streamer):
        """
        Gets streamer login name from Twitch and returns it
        :param streamer:
        :return: streamer login_name
        """
        headers = http_helpers.form_auth_headers(self.client_id, self.access_token)
        response = http_helpers.send_get_request('https://api.twitch.tv/helix/users?id=' + streamer['user_id'],
                                                 headers=headers)
        try:
            data = response.json()['data']
            streamer_login_name = (data[0]['login'])
        except KeyError:
            log.warning('No streamers login found for ' + str(streamer['user_id']))
            streamer_login_name = None
        return streamer_login_name
