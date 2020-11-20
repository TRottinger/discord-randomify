import logging
import os

import discord
from discord.ext import commands
import random
import wikipedia

from utils.gachahelpers.gacharoll import GachaRoll

log = logging.getLogger(__name__)


class Gacha(commands.Cog):
    """
    Main cog Class for Gacha!!
    """
    def __init__(self, bot):
        self.bot = bot
        self.gacha_roll = GachaRoll()

    @commands.command(name="gacha", description="Play gacha! Who knows what you'll get", aliases=["gacharoll"],
                      brief="Random gacha card!")
    async def gacha(self, ctx):
        choice = await self.gacha_roll.gacharoll()
        embed = discord.Embed(title='Gacha Result')
        embed.colour = discord.Colour.dark_purple()
        embed.add_field(name='Name', value=choice['name'], inline=True)
        embed.add_field(name='Source', value=choice['source'], inline=True)
        embed.add_field(name='Rarity', value=choice['rarity'], inline=True)
        img = discord.File('data/imgs/' + choice['id'] + '.jpg', filename='gacha.jpg')
        embed.set_image(url='attachment://gacha.jpg')
        await ctx.send(embed=embed, file=img)


def setup(bot):
    bot.add_cog(Gacha(bot))
