import re

GAME_OPT = 'game='
LANGUAGE_OPT = 'language='


def parse_args(input_string):
    args = {"game": "any", "language": "any"}

    if GAME_OPT in input_string:
        game = input_string.split('game=')[1]
        game = re.findall(r'"([^"]*)"', game)[0]
        args["game"] = game

    if LANGUAGE_OPT in input_string:
        language = input_string.split('language=')[1]
        language = re.findall(r'"([^"]*)"', language)[0]
        args["language"] = language

    return args
