import logging

import discord
from discord import app_commands
import random
import wikipedia

log = logging.getLogger(__name__)


class Wiki(app_commands.Group):
    """
    Main cog Class for wikipedia functionality
    """
    def __init__(self):
        super().__init__()

    @app_commands.command(name="wiki", description="Get a link to a random wiki article")
    async def wiki(self, interaction: discord.Interaction):
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
        embed.add_field(name='Title', value=info.original_title, inline=False)
        embed.add_field(name='Summary', value=info.summary, inline=False)
        embed.set_footer(text='Link hidden for SFW purposes')
        embed.colour = discord.Colour.orange()
        await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(Wiki(bot))
