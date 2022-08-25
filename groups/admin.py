import logging
from tabnanny import check
from typing import Union

import discord
from discord import app_commands

log = logging.getLogger(__name__)



class Admin(app_commands.Group):
    def __init__(self):
        super().__init__()

    def check_is_owner(interaction: discord.Interaction) -> bool:
        return interaction.user.id == 179780915558481929
