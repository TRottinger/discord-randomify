import discord
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
        embed = discord.Embed(title='Random Wikipedia')
        embed.add_field(name=info.original_title, value=info.url, inline=False)
        embed.add_field(name='Summary', value=info.summary, inline=False)
        embed.set_footer(text='Images hidden for SFW purposes')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Wiki(bot))
