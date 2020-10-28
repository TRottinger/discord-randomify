import random

from discord.ext import commands


class CommonRandomizer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="coinflip", description="Flip a coin", aliases=['coin', 'cflip'])
    @commands.guild_only()
    async def coinflip(self, ctx):
        flip = random.randint(0, 1)
        if flip == 0:
            result = 'Heads'
        else:
            result = 'Tails'
        author = ctx.author.mention
        await ctx.send(author + ' ' + result + '')

    @commands.command(name="diceroll", description="Flip a coin", aliases=['dice', 'droll'])
    @commands.guild_only()
    async def diceroll(self, ctx):
        result = random.randint(1, 6)
        author = ctx.author.mention
        await ctx.send(author + ' ' + str(result) + '')


def setup(bot):
    bot.add_cog(CommonRandomizer(bot))
