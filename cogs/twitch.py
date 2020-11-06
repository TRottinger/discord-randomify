import logging

from discord.ext import commands
from utils import twitch_helpers
import random

log = logging.getLogger(__name__)


def prepare_output_string(author, streamer_name, game_name, viewer_count):
    output_string = author + ' I reached into my magic hat and found:\n'
    output_string = output_string + str(streamer_name) + ' playing ' + game_name + ' for ' + str(
        viewer_count) + ' viewers at https://www.twitch.tv/' + streamer_name
    return str(output_string)


class Twitch(commands.Cog):
    """
    Main cog Class for Twitch functionality
    """
    def __init__(self, bot):
        self.bot = bot
        self.twitch_helpers = twitch_helpers.TwitchHelpers()

    @commands.command(name="twitch", description="Get a link to a random streamer", aliases=["stream", "streamer"],
                      brief="Get a random twitch streamer")
    async def twitch(self, ctx):
        """
        Gets a random twitch stream and returns it to the author
        :param ctx:
        :return:
        """
        log.info('Got twitch call')
        games, weighted_id_game_selector = self.twitch_helpers.get_twitch_games()
        log.info('Got weighted_id_game_selector_size ' + str(len(weighted_id_game_selector)))
        game_id_picked = random.choice(weighted_id_game_selector)
        game_name_picked = str(games.get(game_id_picked))
        log.info('Got game: ' + game_name_picked)

        streamer = self.twitch_helpers.get_streamer(game_id_picked)
        author = ctx.author.mention
        if streamer is None:
            await ctx.send(author + ' I did not find any streamers')
        else:
            result_string = prepare_output_string(author, str(streamer.login_name),
                                                  game_name_picked, streamer.viewers)
            log.info('Sending out result string: ' + result_string)
            await ctx.send(result_string)

    @commands.command(name="twitchgame", description="Get a link to a random streamer playing a specific game",
                      aliases=["game_stream", "twitch_game"], usage="<game_name>",
                      brief="Get a random twitch streamer by game")
    async def twitchgame(self, ctx, *, arg):
        """
        Gets a random twitch stream by game and returns it to the author
        Do not use quotes when passing in the game
        The bot will treat everything after twitchgame as the game
        Example: twitchgame League of Legends
        :param ctx:
        :param arg:
        :return:
        """
        game_name_picked = arg
        game_id_picked = self.twitch_helpers.get_game_by_name(game_name_picked)

        author = ctx.author.mention
        if game_id_picked == '':
            await ctx.send(author + ' I did not find the game ' + game_name_picked)
            return
        streamer = self.twitch_helpers.get_streamer(game_id_picked)
        if streamer is None:
            await ctx.send(author + ' I did not find any streamers under the game ' + game_name_picked)
        else:
            result_string = prepare_output_string(author, str(streamer.login_name),
                                                  game_name_picked, streamer.viewers)
            log.info('Sending out result string: ' + result_string)
            await ctx.send(result_string)

    @twitchgame.error
    async def twitchgame_error(self, ctx, error):
        author = ctx.author.mention
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(author + ' - Please provide an argument')


def setup(bot):
    bot.add_cog(Twitch(bot))
