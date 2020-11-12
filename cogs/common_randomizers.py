import random
import time

from discord.ext import commands

import logging

log = logging.getLogger(__name__)


class CommonRandomizer(commands.Cog):
    """
    Class for commonly used and know randomizers.
    Example: Dice roll, coin flip, etc.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.info('Loading Common Randomizers cog')

    async def percent_roll(self, percent):
        """
        Returns a Boolean based on roll
        :param percent:
        :return: Bool
        """
        return random.randrange(100) < percent

    @commands.command(name="coinflip", description="Flip a coin", aliases=['coin', 'cflip'],
                      brief="Classic coin flip")
    async def coinflip(self, ctx):
        """
        Flip the coin! Then send a message to the author with the result
        """
        flip = random.randint(0, 1)
        if flip == 0:
            result = 'Heads'
        else:
            result = 'Tails'
        author = ctx.author.mention
        await ctx.send(author + ' ' + result + '')

    @commands.command(name="diceroll", description="Roll a 6 sided die", aliases=['dice', 'droll'],
                      brief="Roll a six-sided die")
    async def diceroll(self, ctx):
        """
        Roll a six-sided dice, then let the author know the result
        """
        result = random.randint(1, 6)
        author = ctx.author.mention
        await ctx.send(author + ' ' + str(result) + '')

    @commands.command(name="roll", description="Roll a number. Defaults to rolling from 1-100",
                      brief="Provide a number to roll to that amount", usage="[value]")
    async def roll(self, ctx, *, arg=100):
        """
        Roll from 1 to a number. Sends the output to the author
        This defaults to 100
        An arg can be passed to change the default value
        Example: roll 50
            - Rolls from 1-50
        """
        author = ctx.author.mention
        if arg > 1000001:
            await ctx.send(author + ' really? Why do you need to roll that high? Just don\'t')
        else:
            result = random.randint(1, arg)
            await ctx.send(author + ' ' + str(result) + '')

    @commands.command(name="dndroll", description="Roll a dnd dice. Format XdY where X and Y are numbers",
                      brief="Roll a dnd dice. Format [1-9]d[1-20]. Example: dndroll 2d6", usage="[1-9d1-20]")
    async def dndroll(self, ctx, *, arg='1d20'):
        """
        Rolls a DnD dice, then outputs the value to the author
        This defaults to a "1d20" roll
        You can customize this by passing in values as you would in typical DnD games
        Example: dndroll 2d6 (This rolls 2 d6 dice)
        Example: dndroll 1d10 (This rolls 1 d10 die)
        """
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
                      brief="Choose one from list. Space separated input. Example: choose red blue green",
                      usage="<value1> <value2> ... [valueN]")
    async def choose(self, ctx, *args):
        """
        Chooses between a list of arguments randomly, then outputs to author
        Any number of arguments can be passed, but there must be at least 2
        Arguments are separated by spaces
        Example: choose red blue yellow
        """
        author = ctx.author.mention
        if len(args) < 2:
            await ctx.send(author + ' please provide enough arguments')
        else:
            result = random.choice(args)
            await ctx.send(author + ' ' + str(result) + '')

    # @commands.command(name="dramaticchoose", description="Choose between a list of things.. dramatically",
    #                  brief="Choose one from list. Space separated input. Example: dramaticchoose red blue green",
    #                  usage="<value1> <value2> ... [valueN]")
    # async def dramaticchoose(self, ctx, *args):
    #    """
    #    Chooses between a list of arguments randomly, then outputs to author
    #    Any number of arguments can be passed, but there must be at least 2
    #    Arguments are separated by spaces
    #    Example: choose red blue yellow
    #    """
    #    choices = [arg for arg in args]
    #    if len(args) < 2:
    #        await ctx.send('Please provide enough arguments')
    #    elif len(args) > 10:
    #        await ctx.send('That would take too long....')
    #    else:
    #        length = len(args)
    #        for i in range(0, length-1):
    #            await ctx.send('Removing one option from: ' + ', '.join(choices))
    #            result = random.choice(args)
    #            choices.remove(result)
    #            time.sleep(1)
    #            await ctx.send('Removed ' + str(result) + '!')
    #            time.sleep(1)
    #        await ctx.send('And the winner is: ' + ' '.join(choices))

    @commands.command(name="russianroulette", description="Like choose but with russian roulette",
                      brief="Classic Russian roulette. Example: russianroulette jane john",
                      usage="<value1> <value2> ... [value6]")
    async def russianroulette(self, ctx, *args):
        """
        A fun little game of Russian Roulette
        It is not recommended to play this with more than 3 people
        Rotates around in a circle taking shots
        If there is a bullet in the chamber at the time of the shot, that person is shot and the game ends
        Else, the game keeps going
        The bot is very talkative with this commands
        """
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
                await ctx.send(monkas)
                time.sleep(1)
                result = await self.percent_roll((bullets/chamber)*100)
                if result:
                    await ctx.send(':boom:')
                    await ctx.send('Sorry ' + args[index] + ', you lost!')
                    break
                else:
                    await ctx.send(args[index] + ' you are OK')
                    chamber -= 1
                    if index == rotate:
                        index = 0
                    else:
                        index += 1
                    time.sleep(2)


def setup(bot):
    bot.add_cog(CommonRandomizer(bot))
