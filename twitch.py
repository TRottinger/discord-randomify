import requests
import random
import os
from dotenv import load_dotenv
from url_builder import build_twitch_streams_url

load_dotenv()
CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')


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

    for game in games:
        game_dict[game['id']] = game['name']

    return game_dict


def get_twitch_streams(game_id=0):

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

        for data in response.json()['data']:
            streamers.append(data)

        if str(response.json()['pagination']) == '{}':
            break
        else:
            pag = response.json()['pagination']['cursor']
            after = pag

    return streamers


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
