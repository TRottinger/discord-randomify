from discord.ext import commands
import urllib.request
import urllib.error


class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="subreddit", description="Get a link to a random subreddit", brief="Get a random subreddit")
    async def subreddit(self, ctx):
        try:
            urlopen = urllib.request.urlopen('https://www.reddit.com/r/random')
            result = str(urlopen.url)
        except urllib.error.HTTPError:
            result = 'I\'m being rate limited :('
        author = ctx.author.mention
        await ctx.send(author + ' ' + result + '')


def setup(bot):
    bot.add_cog(Reddit(bot))
