import random
import twitch


def get_random_twitch_stream_with_args(args):
    res_string = ''

    game_id_picked = ''
    game_name_picked = ''
    if args['game'] != 'any':
        game_name_picked = args['game']
        game_id_picked = twitch.get_game_by_name(game_name_picked)

    if game_id_picked == '':
        res_string += 'Oops! Sorry, your game ' + args['game'] + ' was not found! :(\n'
        games, weighted_id_game_selector = twitch.get_twitch_games()

        game_id_picked = random.choice(weighted_id_game_selector)
        game_name_picked = str(games.get(game_id_picked))

    streamers = twitch.get_twitch_streams(game_id_picked)

    streamer = random.choice(streamers)

    streamer_login_name = twitch.get_streamer_login_name(streamer)

    print('Returning: ' + str(streamer_login_name), str(streamer['viewer_count']), game_name_picked)
    return str(streamer_login_name), str(streamer['viewer_count']), game_name_picked, res_string


def get_random_twitch_stream():
    res_string = ''

    games, weighted_id_game_selector = twitch.get_twitch_games()

    game_id_picked = random.choice(weighted_id_game_selector)
    game_name_picked = str(games.get(game_id_picked))

    streamers = twitch.get_twitch_streams(game_id_picked)

    streamer = random.choice(streamers)

    streamer_login_name = twitch.get_streamer_login_name(streamer)

    print('Returning: ' + str(streamer_login_name), str(streamer['viewer_count']), game_name_picked)
    return str(streamer_login_name), str(streamer['viewer_count']), game_name_picked, res_string


if __name__ == '__main__':
    get_random_twitch_stream()
