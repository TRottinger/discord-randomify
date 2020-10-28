import random

import requests
import wikipedia
from discord_bot_randomizer import twitch
import urllib.request


def get_streamer(game_id):
    streamers = twitch.get_twitch_streams(game_id)

    if len(streamers) == 0:
        return None, None

    streamer = random.choice(streamers)

    streamer_login_name = twitch.get_streamer_login_name(streamer)

    return streamer, streamer_login_name


def get_random_twitch_stream_by_game(game_selected):

    game_name_picked = game_selected
    game_id_picked = twitch.get_game_by_name(game_name_picked)

    if game_id_picked == '':
        return [None, None, None]

    streamer, streamer_login_name = get_streamer(game_id_picked)
    if streamer_login_name is None:
        return [None, None, None]
    else:
        return [str(streamer_login_name), str(streamer['viewer_count']), game_name_picked]


def get_random_twitch_stream():

    games, weighted_id_game_selector = twitch.get_twitch_games()

    game_id_picked = random.choice(weighted_id_game_selector)
    game_name_picked = str(games.get(game_id_picked))

    streamer, streamer_login_name = get_streamer(game_id_picked)
    if streamer_login_name is None:
        return [None, None, None]
    else:
        return [str(streamer_login_name), str(streamer['viewer_count']), game_name_picked]


def get_random_wiki_article():
    page = wikipedia.random(1)
    info = wikipedia.page(page)
    url = info.url
    return str(url)


def get_random_subreddit():
    result = urllib.request.urlopen('https://www.reddit.com/r/random')
    return str(result.url)


if __name__ == '__main__':
    get_random_twitch_stream()
