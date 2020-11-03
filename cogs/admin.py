from discord.ext import commands


OWNER_IDS = ['179780915558481929']


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Admin(bot))
