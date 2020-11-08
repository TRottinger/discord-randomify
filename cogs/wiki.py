from discord.ext import commands
import random
import wikipedia


class Wiki(commands.Cog):
    """
    Main cog Class for wikipedia functionality
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="wiki", description="Get a link to a random wiki article", aliases=["wikipedia"],
                      brief="Get a random wiki article")
    async def wiki(self, ctx):
        """
        Gets a random wikipedia link and returns it to the user
        """
        page = wikipedia.random(1)
        try:
            info = wikipedia.page(page)
        except wikipedia.DisambiguationError as e:
            s = random.choice(e.options)
            info = wikipedia.page(s)
        url = info.url
        author = ctx.author.mention
        await ctx.send(author + ' ' + str(url) + '')


def setup(bot):
    bot.add_cog(Wiki(bot))
