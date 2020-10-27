import random
from discord_bot_randomizer import twitch


def get_streamer(game_id):
    streamers = twitch.get_twitch_streams(game_id)

    streamer = random.choice(streamers)

    streamer_login_name = twitch.get_streamer_login_name(streamer)

    return streamer, streamer_login_name


def get_random_twitch_stream_by_game(game_selected):

    game_name_picked = game_selected
    game_id_picked = twitch.get_game_by_name(game_name_picked)
    print('Selecting game: ' + game_name_picked)

    if game_id_picked == '':
        return None, None, None

    streamer, streamer_login_name = get_streamer(game_id_picked)
    print('Returning: ' + str(streamer_login_name), str(streamer['viewer_count']), game_name_picked)
    return str(streamer_login_name), str(streamer['viewer_count']), game_name_picked


def get_random_twitch_stream():

    games, weighted_id_game_selector = twitch.get_twitch_games()

    game_id_picked = random.choice(weighted_id_game_selector)
    game_name_picked = str(games.get(game_id_picked))

    streamer, streamer_login_name = get_streamer(game_id_picked)
    print('Returning: ' + str(streamer_login_name), str(streamer['viewer_count']), game_name_picked)
    return str(streamer_login_name), str(streamer['viewer_count']), game_name_picked


if __name__ == '__main__':
    get_random_twitch_stream()
