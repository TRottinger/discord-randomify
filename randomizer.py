import requests
import random
import os
from dotenv import load_dotenv
from url_builder import build_url

load_dotenv()
CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')


def get_random_twitch_stream():

    headers = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }

    response = requests.post('https://id.twitch.tv/oauth2/token', data=headers)

    access_token = response.json()['access_token']

    streams_request_url = 'https://api.twitch.tv/helix/streams'

    headers = {
        'client-id': CLIENT_ID,
        'Authorization': 'Bearer ' + access_token,
    }

    response = requests.get('https://api.twitch.tv/helix/games/top?first=100', headers=headers)
    games = response.json()['data']

    game_ids = []
    game_dict = {}

    for game in games:
        game_ids.append(game['id'])
        game_dict[game['id']] = game['name']

    game_id_picked = random.choice(list(game_dict))
    game_name_picked = str(game_dict.get(game_id_picked))

    after = '0'
    streamers = []

    for i in range(0, 10):

        if after != '0':
            request_url = build_url(streams_request_url, "first=100", "game_id=" + game_id_picked, "after=" + after)
        else:
            request_url = build_url(streams_request_url, "first=100", "game_id=" + game_id_picked)

        response = requests.get(request_url, headers=headers)

        for data in response.json()['data']:
            streamers.append(data)

        if str(response.json()['pagination']) == '{}':
            break
        else:
            pag = response.json()['pagination']['cursor']
            after = pag

    streamer = random.choice(streamers)

    response = requests.get('https://api.twitch.tv/helix/users?id=' + streamer['user_id'], headers=headers)
    data = response.json()['data']
    streamer_login_name = (data[0]['login'])

    print('Returning: ' + str(streamer_login_name), str(streamer['viewer_count']), game_name_picked)
    return str(streamer_login_name), str(streamer['viewer_count']), game_name_picked


if __name__ == '__main__':
    get_random_twitch_stream()
