from discord.ext import commands
from urllib.request import Request
import urllib.error


class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reddit", description="Get a link to a random subreddit", brief="Get a random subreddit",
                      aliases=["subreddit"])
    async def reddit(self, ctx):
        try:
            urlopen = urllib.request.Request('https://www.reddit.com/r/random')
            urlopen.add_header('User-Agent', 'discord-bot/0.0.1')
            if urlopen.full_url.startswith('https'):
                with urllib.request.urlopen(urlopen) as response:
                    result = str(response.url)
        except urllib.error.HTTPError:
            result = 'I\'m being rate limited, so manually click this: https://www.reddit.com/r/random'
        author = ctx.author.mention
        await ctx.send(author + ' ' + result + '')


def setup(bot):
    bot.add_cog(Reddit(bot))
