import random
import time

from discord.ext import commands


class CommonRandomizer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def percent_roll(self, percent):
        return random.randrange(100) < percent

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
        else:
            result = random.randint(1, arg)
            await ctx.send(author + ' ' + str(result) + '')

    @commands.command(name="dndroll", description="Roll a dnd dice. Format XdY where X and Y are numbers",
                      brief="Roll a dnd dice. Format [1-9]d[1-20]", usage="[1-9]d[1-20]")
    async def dndroll(self, ctx, *, arg='1d20'):
        ints = arg.split('d')
        author = ctx.author.mention
        if len(ints) != 2:
            await ctx.send(author + ' invalid arguments. Try again! Example: 1d6')
        times = ints[0]
        dice = ints[1]
        if not times.isdigit() or not dice.isdigit():
            await ctx.send(author + ' invalid arguments. Try again! Example: 1d6')
        times = int(times)
        dice = int(dice)
        if times > 9 or dice > 20:
            await ctx.send(author + ' numbers too high!')
        else:
            result = times * random.randint(1, dice)
            await ctx.send(author + ' your ' + str(times) + 'd' + str(dice) + ' roll returned ' + str(result) + '')

    @commands.command(name="choose", description="Choose between a list of things",
                      brief="Choose one from list. Space separated input")
    async def choose(self, ctx, *args):
        author = ctx.author.mention
        if len(args) < 2:
            await ctx.send(author + ' please provide enough arguments')
        else:
            result = random.choice(args)
            await ctx.send(author + ' ' + str(result) + '')

    @commands.command(name="russianroulette", description="Like choose but with a gun",
                      brief="Classic Russian roulette")
    async def russianroulette(self, ctx, *args):
        author = ctx.author.mention
        bullets = 1
        chamber = 6
        emojis = self.bot.emojis
        monkas = None
        for emoji in emojis:
            if emoji.name == 'monkaS':
                monkas = str(emoji)
                break
        if monkas is None:
            monkas = ':person_bald:'

        if len(args) < 2:
            await ctx.send(author + ' please provide enough arguments')
        else:
            random.shuffle(list(args))
            rotate = len(args) - 1
            index = 0
            while bullets == 1:
                await ctx.send('Alright, ' + args[index] + ', you\'re up. ' + str(chamber) + ' shots left.....')
                time.sleep(1)
                await ctx.send(monkas + ' :gun:')
                time.sleep(1)
                result = await self.percent_roll((bullets/chamber)*100)
                if result:
                    await ctx.send(':boom: :skull: :gun:')
                    await ctx.send('Sorry ' + args[index] + ', you died!')
                    break
                else:
                    await ctx.send(args[index] + ' you lived!')
                    chamber -= 1
                    if index == rotate:
                        index = 0
                    else:
                        index += 1
                    time.sleep(2)


def setup(bot):
    bot.add_cog(CommonRandomizer(bot))
