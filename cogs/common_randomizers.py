import random

from discord.ext import commands


class CommonRandomizer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="coinflip", description="Flip a coin", aliases=['coin', 'cflip'],
                      brief="Always heads")
    async def coinflip(self, ctx):
        flip = random.randint(0, 1)
        if flip == 0:
            result = 'Heads'
        else:
            result = 'Tails'
        author = ctx.author.mention
        await ctx.send(author + ' ' + result + '')

    @commands.command(name="diceroll", description="Flip a coin", aliases=['dice', 'droll'],
                      brief="Roll a six-sided die")
    async def diceroll(self, ctx):
        result = random.randint(1, 6)
        author = ctx.author.mention
        await ctx.send(author + ' ' + str(result) + '')

    @commands.command(name="roll", description="Roll a number. Defaults to rolling from 1-100",
                      brief="Provide a number to roll to that amount", usage="max")
    async def roll(self, ctx, *, arg=100):
        author = ctx.author.mention
        if arg > 1000001:
            await ctx.send(author + ' really? Why do you need to roll that high? Just don\'t')
        result = random.randint(1, arg)
        await ctx.send(author + ' ' + str(result) + '')


def setup(bot):
    bot.add_cog(CommonRandomizer(bot))
