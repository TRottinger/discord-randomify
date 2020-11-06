from urllib.request import Request
import urllib.error
from discord.ext import commands


class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="anime", description="Get a random anime", brief="Get a random anime")
    async def anime(self, ctx):
        """
        Gets a random anime from anidb.net
        :param ctx:
        :return:
        """
        try:
            urlopen = urllib.request.Request('https://anidb.net/anime/random')
            urlopen.add_header('User-Agent', 'discord-bot/0.0.1')
            if urlopen.full_url.startswith('https'):
                with urllib.request.urlopen(urlopen) as response:
                    result = str(response.url)
        except urllib.error.HTTPError:
            result = 'I\'m being rate limited, so manually click this: https://anidb.net/anime/random'
        author = ctx.author.mention
        await ctx.send(author + ' enjoy! ' + result + '')


def setup(bot):
    bot.add_cog(Anime(bot))
