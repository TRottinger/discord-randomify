import logging
from discord.ext import commands, tasks
from utils import twitch_helpers
import random

from utils.http_helpers import get_access_token

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


class Twitch(commands.Cog):
    """
    Main cog Class for Twitch functionality
    """
    def __init__(self, bot):
        self.bot = bot
        self.twitch_helpers = twitch_helpers.TwitchHelpers()
        log.info('Loading Twitch cog')
        self.reset_auth_code.start()

    def cog_unload(self):
        self.reset_auth_code.cancel()

    @tasks.loop(hours=24)
    async def reset_auth_code(self):
        await self.twitch_helpers.refresh_access_token()

    # Twitch is the only API we use that could get overloaded
    # All of the others have manually set rate limits
    # Lets be safe and apply a cooldown of 3 usages per minute per user
    @commands.cooldown(3, 60, commands.BucketType.user)
    @commands.command(name="twitch", description="Get a link to a random streamer", aliases=["stream", "streamer"],
                      brief="Get a random twitch streamer")
    async def twitch(self, ctx):
        """
        Gets a random twitch stream and returns it to the author
        Limit is 3 calls per minute
        """
        games, weighted_id_game_selector = self.twitch_helpers.get_twitch_games()
        if games is None or weighted_id_game_selector is None:
            log.warning('Trouble getting random game')
            if len(self.twitch_helpers.local_stream_cache) == 0:
                await ctx.send('I had trouble processing the request')
                return
            else:
                streamer = self.twitch_helpers.get_streamer(game_id=0, cache=True)
                if streamer is None:
                    await ctx.send('I had trouble processing the request')
                    return
                else:
                    await ctx.send('I had trouble processing the request. Selecting from cache')
                game_name_picked = None
        else:
            game_id_picked = random.choice(weighted_id_game_selector)
            game_name_picked = str(games.get(game_id_picked))

            streamer = self.twitch_helpers.get_streamer(game_id_picked)

        author = ctx.author.mention

        if streamer is None:
            log.warning('Trouble getting random streamer')
            await ctx.send(author + ' I did not find any streamers')
        else:
            result_string = prepare_output_string(author, str(streamer.login_name),
                                                  game_name_picked, streamer.viewers)
            await ctx.send(result_string)

    @commands.cooldown(3, 60, commands.BucketType.user)
    @commands.command(name="twitchgame", description="Get a link to a random streamer playing a specific game",
                      aliases=["game_stream", "twitch_game"], usage="<game_name>",
                      brief="Get a random twitch streamer by game")
    async def twitchgame(self, ctx, *, arg):
        """
        Gets a random twitch stream by game and returns it to the author
        Do not use quotes when passing in the game
        The bot will treat everything after twitchgame as the game
        Example: twitchgame League of Legends
        Limit is 3 calls per minute
        """
        game_name_picked = arg
        game_id_picked = self.twitch_helpers.get_game_by_name(game_name_picked)

        author = ctx.author.mention
        if game_id_picked is None:
            log.warning('Trouble getting game')
            if len(self.twitch_helpers.local_stream_cache) == 0:
                await ctx.send('I had trouble finding the game ' + game_name_picked)
                return
            else:
                streamer = self.twitch_helpers.get_streamer(game_id=0, cache=True)
                if streamer is None:
                    await ctx.send('I had trouble processing the request')
                    return
                else:
                    await ctx.send('I had trouble processing the request. Selecting from cache')
                game_name_picked = None
        else:
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
