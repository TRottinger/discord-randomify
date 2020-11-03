from discord.ext import commands


class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="anime", description="Get a random anime", brief="Get a random anime")
    async def anime(self, ctx):
        print('stub')


def setup(bot):
    bot.add_cog(Anime(bot))