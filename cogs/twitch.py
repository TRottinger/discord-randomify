from discord.ext import commands
from utils import twitch_helpers
import random


class Twitch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="twitch", description="Get a link to a random streamer", aliases=["stream", "streamer"],
                      brief="Get a random twitch streamer")
    async def twitch(self, ctx):
        games, weighted_id_game_selector = twitch_helpers.get_twitch_games()

        game_id_picked = random.choice(weighted_id_game_selector)
        game_name_picked = str(games.get(game_id_picked))

        streamer = twitch_helpers.get_streamer(game_id_picked)
        author = ctx.author.mention
        if streamer is None:
            await ctx.send(author + ' I did not find any streamers')
        else:
            result_string = author + ' I reached into my magic hat and found:\n'
            result_string = result_string + str(streamer.login_name) + ' playing ' + game_name_picked + ' for ' + str(
                streamer.viewers) + ' viewers at https://www.twitch.tv/' + streamer.login_name
            await ctx.send(result_string)

    @commands.command(name="twitch_game", description="Get a link to a random streamer playing a specific game",
                      aliases=["game_stream", "twitchgame"], usage="<game_name>",
                      brief="Get a random twitch streamer by game")
    async def twitch_game(self, ctx, *, arg):
        game_name_picked = arg
        game_id_picked = twitch_helpers.get_game_by_name(game_name_picked)

        author = ctx.author.mention
        if game_id_picked == '':
            await ctx.send(author + ' I did not find the game ' + game_name_picked)
            return
        streamer = twitch_helpers.get_streamer(game_id_picked)
        if streamer is None:
            await ctx.send(author + ' I did not find any streamers under the game ' + game_name_picked)
        else:
            result_string = author + ' I reached into my magic hat and found:\n'
            result_string = result_string + str(streamer.login_name) + ' playing ' + game_name_picked + ' for ' + str(
                streamer.viewers) + ' viewers at https://www.twitch.tv/' + streamer.login_name
            await ctx.send(result_string)

    @twitch_game.error
    async def twitch_game_error(self, ctx, error):
        author = ctx.author.mention
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(author + ' - Please provide an argument')


def setup(bot):
    bot.add_cog(Twitch(bot))
