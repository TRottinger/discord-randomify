from discord.ext import commands
import random
import wikipedia


class Wiki(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="wiki", description="Get a link to a random wiki article", aliases=["wikipedia"])
    @commands.guild_only()
    async def wiki(self, ctx):
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
