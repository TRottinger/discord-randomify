from discord.ext import commands

import logging

log = logging.getLogger(__name__)


class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.info('Loading Configuration cog')

    @commands.command(hidden=True)
    async def ping(self, ctx):
        """
        Pong!
        """
        await ctx.send('Pong')

    @commands.command(name='prefix', description='Set the prefix for this guild',
                      brief='Set prefix for invocation. Example prefix ~', aliases=['prefix_set'])
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, prefix):
        """
        Set the prefix for the guild
        Currently, this is open for everyone to access. Need to change to be only those with permissions
        The prefix is saved between bot instances
        Example: !rt prefix ~ to set the prefix to ~
        """
        result = await self.bot.set_guild_prefix(ctx.guild.id, prefix)
        if result is True:
            await ctx.send('The prefix has been set to ' + str(prefix))
        else:
            await ctx.send('Invalid prefix. Sorry :(')

    @prefix.error
    async def prefix_error(self, ctx, error):
        author = ctx.author.mention
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(author + ' - Please provide an argument')

    @commands.command(name='get_prefix', description='Get the prefix for this guild',
                      brief='Get prefix for invocation', aliases=['prefix_get'])
    @commands.guild_only()
    async def get_prefix(self, ctx):
        """
        Returns the default prefix and custom prefix for the current guild and sends it to the author
        """
        prefix = self.bot.get_guild_prefix(ctx.guild.id)
        author = ctx.author.mention
        if self.bot.default_prefix == prefix:
            await ctx.send(author + ' available prefixes are: \"' + self.bot.default_prefix + '\"')
        else:
            await ctx.send(author + ' available prefixes are: \"' + self.bot.default_prefix + '\" and \"'
                           + prefix + '\"')

    @commands.command(name='github', description='Get the code for the me!',
                      brief='Get my code', aliases=['git'])
    async def github(self, ctx):
        """
        Sends the link to the GitHub to the author
        """
        github = 'https://github.com/TRottinger/discord-randomify'
        author = ctx.author.mention
        await ctx.send(author + ' check out my code on GitHub: ' + github)

    @commands.command(name='discord', description='Invite link to the bot discord',
                      brief='Bot discord')
    async def discord(self, ctx):
        """
        Sends the link to the Discord to the author
        """
        discord = 'https://discord.gg/EbZ3QX4'
        author = ctx.author.mention
        await ctx.send(author + ' join our Discord server: ' + discord)

    @commands.command(name='invite', description='Invite link to have bot join your Discord',
                      brief='Invite link for bot')
    async def invite(self, ctx):
        """
        Sends the invite link for the bot to the channel
        """
        await ctx.send('To invite the bot to your server, use: https://discord.com/oauth2/authorize?client_id=770197604155785216&permissions=11328&scope=bot')


def setup(bot):
    bot.add_cog(Config(bot))
