import random
import time
from typing import Optional

import discord
from discord import app_commands

import logging

log = logging.getLogger(__name__)


class CommonRandomizer(app_commands.Group):
    """
    Class for commonly used and know randomizers.
    Example: Dice roll, coin flip, etc.
    """
    def __init__(self):
        super().__init__()
        log.info("Loading command randomizers")

    async def percent_roll(self, percent):
        """
        Returns a Boolean based on roll
        :param percent:
        :return: Bool
        """
        return random.randrange(100) < percent

    @app_commands.command(name="coinflip", description="Flip a coin")
    async def coinflip(self, interaction: discord.Interaction):
        """
        Flip the coin! Then send a message to the author with the result
        """
        flip = random.randint(0, 1)
        if flip == 0:
            result = 'Heads'
        else:
            result = 'Tails'
        await interaction.response.send_message(interaction.user.mention + ' ' + result + '')

    @app_commands.command(name="diceroll", description="Roll a 6 sided die")
    async def diceroll(self, interaction: discord.Interaction):
        """
        Roll a six-sided dice, then let the author know the result
        """
        result = random.randint(1, 6)
        author = interaction.user.mention
        await interaction.response.send_message(author + ' ' + str(result) + '')

    @app_commands.command(name="roll", description="Roll a number. Defaults to rolling from 1-100")
    @app_commands.describe(arg="Roll between 1 and this number")
    async def roll(self, interaction: discord.Interaction, arg: Optional[int] = 100):
        """
        Roll from 1 to a number. Sends the output to the author
        This defaults to 100
        An arg can be passed to change the default value
        Example: roll 50
            - Rolls from 1-50
        """
        author = interaction.user.mention
        if arg > 1000001:
            await interaction.response.send_message(author + ' really? Why do you need to roll that high? Just don\'t')
        else:
            result = random.randint(1, arg)
            await interaction.response.send_message(author + ' ' + str(result) + '')

    @app_commands.command(name="dndroll", description="Roll a dnd dice. Format XdY where X and Y are numbers")
    @app_commands.describe(arg="NdK where N is how many rolls and K is K-sided dice (i.e. 1d10)")
    async def dndroll(self, interaction: discord.Interaction, arg: Optional[str] = '1d20'):
        """
        Rolls a DnD dice, then outputs the value to the author
        This defaults to a "1d20" roll
        You can customize this by passing in values as you would in typical DnD games
        Example: dndroll 2d6 (This rolls 2 d6 dice)
        Example: dndroll 1d10 (This rolls 1 d10 die)
        """
        ints = arg.split('d')
        author = interaction.user.mention
        if len(ints) != 2:
            await interaction.response.send_message(author + ' invalid arguments. Try again! Example: 1d6')
            return
        times = ints[0]
        dice = ints[1]
        if not times.isdigit() or not dice.isdigit():
            await interaction.response.send_message(author + ' invalid arguments. Try again! Example: 1d6')
            return
        times = int(times)
        dice = int(dice)
        if times > 9 or dice > 20:
            await interaction.response.send_message(author + ' numbers too high!')
        else:
            result = times * random.randint(1, dice)
            await interaction.response.send_message(author + ' your ' + str(times) + 'd' + str(dice) + ' roll returned ' + str(result) + '')

    # @app_commands.command(name="choose", description="Choose between a list of things")
    # async def choose(self, interaction: discord.Interaction, args: str):
    #     """
    #     Chooses between a list of arguments randomly, then outputs to author
    #     Any number of arguments can be passed, but there must be at least 2
    #     Arguments are separated by spaces
    #     Example: choose red blue yellow
    #     """
    #     author = interaction.user.mention
    #     if len(args) < 2:
    #         await interaction.response.send_message(author + ' please provide enough arguments')
    #     else:
    #         result = random.choice(args)
    #         await interaction.response.send_message(author + ' ' + str(result) + '')

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
