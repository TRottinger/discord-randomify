import requests
import os
from dotenv import load_dotenv
from utils.url_builder import build_twitch_streams_url
import random
import logging

log = logging.getLogger(__name__)

load_dotenv()


class Streamer:
    def __init__(self, name=None, viewers=None):
        self.login_name = name
        self.viewers = viewers


def get_twitch_access_token(client_id, client_secret, url='https://id.twitch.tv/oauth2/token'):
    """
    Gets access token for twitch and returns it
    :param client_id:
    :param client_secret:
    :param url:
    :return: access_token
    """
    headers = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, data=headers)

    access_token = response.json()['access_token']
    if access_token == '':
        log.warning('Bad access token')

    return access_token


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
        self.access_token = get_twitch_access_token(self.client_id, self.client_secret)

    # Returns a dictionary of top 100 twitch games
    def get_twitch_games(self):
        """
        Returns a list of games and their weights
        :return: dictionary of game id to game name, and weighted game ids
        """
        headers = {
            'client-id': self.client_id,
            'Authorization': 'Bearer ' + self.access_token,
        }

        response = requests.get('https://api.twitch.tv/helix/games/top?first=100', headers=headers)
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
        headers = {
            'client-id': self.client_id,
            'Authorization': 'Bearer ' + self.access_token,
        }
        response = requests.get('https://api.twitch.tv/helix/games?name=' + game_name, headers=headers)
        games = response.json()['data']
        if len(games) > 0:
            log.info('Returning game id: ' + games[0]['id'])
            return games[0]['id']
        return ''

    # Returns a list of streamers
    def get_twitch_streams(self, game_id=0, language=''):
        """
        Gets a list of twitch streams under game_id in the specified language
        :param game_id:
        :param language:
        :return: List of streams
        """
        streams_request_url = 'https://api.twitch.tv/helix/streams'

        headers = {
            'client-id': self.client_id,
            'Authorization': 'Bearer ' + self.access_token,
        }

        after = '0'
        streamers = []

        for i in range(0, 10):
            request_url = build_twitch_streams_url(streams_request_url, '100', str(game_id), after)

            response = requests.get(request_url, headers=headers)

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
            return None

        streamer = random.choice(streamers)
        log.info('Got streamer: ' + str(streamer))

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
        headers = {
            'client-id': self.client_id,
            'Authorization': 'Bearer ' + self.access_token,
        }
        response = requests.get('https://api.twitch.tv/helix/users?id=' + streamer['user_id'], headers=headers)
        data = response.json()['data']
        streamer_login_name = (data[0]['login'])
        return streamer_login_name
