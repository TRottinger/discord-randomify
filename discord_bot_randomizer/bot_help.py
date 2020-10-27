def prepare_help_string():
    help_string = """
    Trigger command: !rt
    Options available for Randomizer bot:
    \t!rt help - List a helpful page of information
    \t!rt random - Gives you something random! (right now just twitch)
    \t!rt game <game_name> - Gives you a random game under game_name (example !rt game league of legends)
    
    Thank you for using the bot! If you have any questions or comments, please reach out to Echolyn#6969
    """
    return help_string


def prepare_result_string(author, streamer, game, viewers):

    result_string = author + ' I reached into my magic hat and found:\n'
    result_string = result_string + streamer + ' playing ' + game + ' for ' + viewers + ' viewers at https://www.twitch.tv/' + streamer
    return result_string
