import re

GAME_OPT = 'game='


def parse_args(input_string):
    args = {"game": "any", "language": "any"}

    if GAME_OPT in input_string and "*" in input_string:
        game = input_string.split('game=')[1]
        game = re.findall(r'"([^"]*)"', game)
        if len(game) != 0:
            args["game"] = game[0]

    return args
