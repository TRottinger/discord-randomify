import re

GAME_OPT = 'game='
AVAILABLE_OPTS = ['game', 'help', 'random']


def parse_args(input_string):
    args = {"game": "any", "language": "any"}

    if GAME_OPT in input_string:
        game = input_string.split('game=')[1]
        game = re.findall(r'"([^"]*)"', game)
        print(game)
        if len(game) != 0:
            args["game"] = game[0]

    return args


def validate_input(input_string, activation_cmd):
    if input_string == activation_cmd or input_string == activation_cmd + ' ':
        return 'no_opt'

    params = input_string.split(activation_cmd + ' ')
    print(params)
    if len(params) == 1:
        return 'bad_opt'
    return params.pop()


def choose_from_available_opts(input_string):
    if input_string.startswith('help'):
        opt = 'help'
        params = ''
    elif input_string.startswith('random'):
        opt = 'random'
        params = ''
    elif input_string.startswith('diceroll'):
        opt = 'diceroll'
        params = ''
    elif input_string.startswith('coinflip'):
        opt = 'coinflip'
        params = ''
    elif input_string.startswith('wiki'):
        opt = 'wiki'
        params = ''
    elif input_string.startswith('reddit'):
        opt = 'reddit'
        params = ''
    elif input_string.startswith('streamer'):
        opt = 'streamer'
        params = ''
    elif input_string.startswith('game '):
        opt = 'game'
        split_string = input_string.split('game ')
        if len(split_string) < 2:
            opt = 'bad_opt'
            params = ''
        else:
            params = split_string[1]
    else:
        opt = 'bad_opt'
        params = ''

    return opt, params


def select_option(input_string, activation_cmd):
    passed_parameters = validate_input(input_string, activation_cmd)
    if passed_parameters == 'no_opt' or passed_parameters == 'bad_opt':
        selected_option = passed_parameters
        selected_parameters = ''
    else:
        selected_option, selected_parameters = choose_from_available_opts(passed_parameters)
    return selected_option, selected_parameters
