import discord
from discord import app_commands

import logging

log = logging.getLogger(__name__)


class Config(app_commands.Group):

    def __init__(self):
        super().__init__()
        log.info("Loading config")

    @app_commands.command(name='ping')
    async def ping(self, interaction: discord.Interaction):
        """
        Pong!
        """
        await interaction.response.send_message('Pong')

    @app_commands.command(name='github', description='Get the code for the me!')
    async def github(self, interaction: discord.Interaction):
        """
        Sends the link to the GitHub to the author
        """
        github = 'https://github.com/TRottinger/discord-randomify'
        await interaction.response.send_message(interaction.user.mention + ' check out my code on GitHub: ' + github)

    @app_commands.command(name='invite', description='Invite link to have bot join your Discord')
    async def invite(self, interaction: discord.Interaction):
        """
        Sends the invite link for the bot to the channel
        """
        await interaction.response.send_message('To invite the bot to your server, use: https://discord.com/oauth2/authorize?client_id=770197604155785216&permissions=11328&scope=bot')

    @app_commands.command(name='discord', description='Invite link to the bot discord')
    async def discordServer(self, interaction: discord.Interaction):
        """
        Sends the link to the Discord to the author
        """
        discord = 'https://discord.gg/EbZ3QX4'
        await interaction.response.send_message(interaction.user.mention + ' join our Discord server: ' + discord)

    @app_commands.command(name='vote', description='Vote for my bot :)')
    async def vote(self, interaction: discord.Interaction):
        """
        Sends the invite link for the bot to the channel
        """
        await interaction.response.send_message('If you enjoy using the bot, please visit https://top.gg/bot/770197604155785216 to review/upvote')

