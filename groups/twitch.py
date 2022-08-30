import logging
from discord.ext import tasks
import discord
from discord import app_commands
from utils import twitch_helpers
import random

log = logging.getLogger(__name__)


def prepare_output_string(author, streamer_name, game_name, viewer_count):
    output_string = author + ' Check out '
    if game_name is not None:
        output_string = output_string + str(streamer_name) + ' playing ' + game_name + ' for ' + str(
            viewer_count) + ' viewers at https://www.twitch.tv/' + streamer_name
    else:
        output_string = output_string + str(streamer_name) + ' streaming for ' + str(viewer_count) + \
                        ' viewers at https://www.twitch.tv/' + streamer_name
    return str(output_string)


class Twitch(app_commands.Group):
    """
    Main cog Class for Twitch functionality
    """
    def __init__(self):
        super().__init__()
        self.twitch_helpers = twitch_helpers.TwitchHelpers()
        log.info('Loading Twitch cog')
        self.reset_auth_code.start()

    def cog_unload(self):
        self.reset_auth_code.cancel()

    @tasks.loop(hours=24)
    async def reset_auth_code(self):
        log.info("resetting auth code")
        await self.twitch_helpers.refresh_access_token()

    @app_commands.checks.cooldown(3, 30)
    @app_commands.command(name="stream", description="Get a link to a random streamer")
    async def stream(self, interaction: discord.Interaction):
        """
        Gets a random twitch stream and returns it to the author
        Limit is 3 calls per minute
        """
        games, weighted_id_game_selector = self.twitch_helpers.get_twitch_games()
        if games is None or weighted_id_game_selector is None:
            log.warning('Trouble getting random game')
            if len(self.twitch_helpers.local_stream_cache) == 0:
                await interaction.response.send_message('I had trouble processing the request')
                return
            else:
                streamer = self.twitch_helpers.get_streamer(game_id=0, cache=True)
                if streamer is None:
                    await interaction.response.send_message('I had trouble processing the request')
                    return
                game_name_picked = None
        else:
            game_id_picked = random.choice(weighted_id_game_selector)
            game_name_picked = str(games.get(game_id_picked))

            streamer = self.twitch_helpers.get_streamer(game_id_picked)

        author = interaction.user.mention

        if streamer is None:
            log.warning('Trouble getting random streamer')
            await interaction.response.send_message(author + ' I did not find any streamers')
        else:
            result_string = prepare_output_string(author, str(streamer.login_name),
                                                  game_name_picked, streamer.viewers)
            await interaction.response.send_message(result_string)

    @app_commands.checks.cooldown(3, 30)
    @app_commands.command(name="game", description="Get a link to a random streamer playing a specific game")
    @app_commands.describe(game='The name of the game you want to watch')
    async def game(self, interaction: discord.Interaction, game: str):
        """
        Gets a random twitch stream by game and returns it to the author
        Do not use quotes when passing in the game
        The bot will treat everything after twitchgame as the game
        Example: twitchgame League of Legends
        Limit is 3 calls per minute
        """
        game_name_picked = game
        game_id_picked = self.twitch_helpers.get_game_by_name(game_name_picked)

        author = interaction.user.mention
        if game_id_picked is None:
            log.warning('Trouble getting game')
            await interaction.response.send_message('I had trouble finding the game ' + game_name_picked)
            return
        streamer = self.twitch_helpers.get_streamer(game_id_picked)
        if streamer is None:
            await interaction.response.send_message(author + ' I did not find any streamers under the game ' + game_name_picked)
        else:
            result_string = prepare_output_string(author, str(streamer.login_name),
                                                  game_name_picked, streamer.viewers)
            log.info('Sending out result string: ' + result_string)
            await interaction.response.send_message(result_string)
