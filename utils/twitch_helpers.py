import requests
import os
from dotenv import load_dotenv
from utils.url_builder import build_twitch_streams_url
import random


# Load twitch client id and secret into file
load_dotenv()
CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')


class Streamer:
    def __init__(self, name=None, viewers=None):
        self.login_name = name
        self.viewers = viewers


def get_twitch_access_token():
    headers = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }

    response = requests.post('https://id.twitch.tv/oauth2/token', data=headers)

    access_token = response.json()['access_token']

    return access_token


# Returns a dictionary of top 100 twitch games
def get_twitch_games():
    access_token = get_twitch_access_token()

    headers = {
        'client-id': CLIENT_ID,
        'Authorization': 'Bearer ' + access_token,
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

    return game_dict, weighted_game_ids


def get_game_by_name(game_name):
    access_token = get_twitch_access_token()

    headers = {
        'client-id': CLIENT_ID,
        'Authorization': 'Bearer ' + access_token,
    }
    response = requests.get('https://api.twitch.tv/helix/games?name=' + game_name, headers=headers)
    games = response.json()['data']
    if len(games) > 0:
        return games[0]['id']
    else:
        return ''


# Returns a list of streamers
def get_twitch_streams(game_id=0, language=''):

    streams_request_url = 'https://api.twitch.tv/helix/streams'

    access_token = get_twitch_access_token()

    headers = {
        'client-id': CLIENT_ID,
        'Authorization': 'Bearer ' + access_token,
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
            return None

        if str(response.json()['pagination']) == '{}':
            break
        else:
            pag = response.json()['pagination']['cursor']
            after = pag

    return streamers


def get_streamer(game_id):
    streamers = get_twitch_streams(game_id)

    if streamers is None:
        return None

    streamer = random.choice(streamers)

    streamer_login_name = get_streamer_login_name(streamer)
    viewer_count = streamer['viewer_count']

    my_streamer = Streamer(streamer_login_name, viewer_count)

    return my_streamer


# Returns streamers user name for twitch link
def get_streamer_login_name(streamer):
    access_token = get_twitch_access_token()

    headers = {
        'client-id': CLIENT_ID,
        'Authorization': 'Bearer ' + access_token,
    }
    response = requests.get('https://api.twitch.tv/helix/users?id=' + streamer['user_id'], headers=headers)
    data = response.json()['data']
    streamer_login_name = (data[0]['login'])
    return streamer_login_name
