import logging

from discord.ext import commands

log = logging.getLogger(__name__)


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.info('Loading Admin cog')

    @commands.is_owner()
    @commands.command(hidden=True)
    async def load_extension(self, ctx, *, extension):
        """
        Load extension
        :param ctx:
        :param extension:
        :return:
        """
        try:
            self.bot.load_extension(extension)
        except commands.ExtensionError as e:
            await ctx.send('Invalid extension. Error: ' + str(e))

    @commands.is_owner()
    @commands.command(hidden=True)
    async def reload_extension(self, ctx, *, extension):
        """
        Reload extension by name
        :param ctx:
        :param extension:
        :return:
        """
        try:
            self.bot.reload_extension(extension)
        except commands.ExtensionError:
            await ctx.send('Invalid extension')

    @commands.is_owner()
    @commands.command(hidden=True)
    async def unload_extension(self, ctx, *, extension):
        """
        Unload extension by name
        :param ctx:
        :param extension:
        :return:
        """
        try:
            self.bot.unload_extension(extension)
        except commands.ExtensionError:
            await ctx.send('Invalid extension')

    @commands.is_owner()
    @commands.command(hidden=True)
    async def load_all_extensions(self, ctx):
        """
        Load extensions
        """
        try:
            self.bot.setup_extensions()
        except commands.ExtensionAlreadyLoaded:
            pass

    @commands.is_owner()
    @commands.command(hidden=True)
    async def unload_all_extensions(self, ctx):
        """
        Unload extensions
        """
        try:
            extensions = self.bot.extensions
            extensions.remove('cogs.admin')
            for extension in extensions:
                self.bot.unload_extension(extension)
        except commands.ExtensionError:
            pass

    @commands.is_owner()
    @commands.command(hidden=True)
    async def get_guilds(self, ctx):
        """
        Get all the guilds that the bot is in
        :param ctx:
        :return:
        """
        guilds = self.bot.guilds
        await ctx.author.send([guild.name for guild in guilds])

    @commands.is_owner()
    @commands.command(hidden=True)
    async def get_cogs(self, ctx):
        """
        Get all the cogs that the bot currently has loaded
        :param ctx:
        :return:
        """
        cogs = self.bot.cogs
        await ctx.author.send([str(cog) for cog in cogs])

    @commands.is_owner()
    @commands.command(hidden=True)
    async def get_commands(self, ctx):
        """
        Get all the commands that the bot has access to
        :param ctx:
        :return:
        """
        cmds = self.bot.commands
        await ctx.author.send([str(command) for command in cmds])

    @commands.is_owner()
    @commands.command(hidden=True)
    async def get_extensions(self, ctx):
        """
        List all of the extensions that the bot has access to
        :param ctx:
        :return:
        """
        extensions = self.bot.extensions
        await ctx.author.send([str(extension) for extension in extensions])

    @commands.is_owner()
    @commands.command(hidden=True)
    async def get_latency(self, ctx):
        """
        Returns latency of bot
        :param ctx:
        :return:
        """
        latency = self.bot.latency
        await ctx.author.send(str(latency))

    @commands.is_owner()
    @commands.command(hidden=True)
    async def get_large_guilds(self, ctx):
        """
        Returns latency of bot
        :param ctx:
        :return:
        """
        guilds = self.bot.guilds
        large_guilds = []
        for guild in guilds:
            if guild.large is True:
                large_guilds.append(guild)

        if len(large_guilds) > 0:
            await ctx.author.send('Here are the large guilds: ' + str (large_guilds))
        else:
            await ctx.author.send('No large guilds')


def setup(bot):
    bot.add_cog(Admin(bot))
