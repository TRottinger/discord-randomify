import random
import twitch


def get_random_twitch_stream():

    games, weighted_id_game_selector = twitch.get_twitch_games()

    game_id_picked = random.choice(weighted_id_game_selector)
    game_name_picked = str(games.get(game_id_picked))

    streamers = twitch.get_twitch_streams(game_id_picked)

    streamer = random.choice(streamers)

    streamer_login_name = twitch.get_streamer_login_name(streamer)

    print('Returning: ' + str(streamer_login_name), str(streamer['viewer_count']), game_name_picked)
    return str(streamer_login_name), str(streamer['viewer_count']), game_name_picked


if __name__ == '__main__':
    get_random_twitch_stream()
