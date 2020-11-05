from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(hidden=True)
    async def load_extension(self, ctx, *, extension):
        try:
            self.bot.load_extension(extension)
        except commands.ExtensionError as e:
            await ctx.send('Invalid extension')

    @commands.is_owner()
    @commands.command(hidden=True)
    async def reload_extension(self, ctx, *, extension):
        try:
            self.bot.reload_extension(extension)
        except commands.ExtensionError as e:
            await ctx.send('Invalid extension')

    @commands.is_owner()
    @commands.command(hidden=True)
    async def unload_extension(self, ctx, *, extension):
        try:
            self.bot.unload_extension(extension)
        except commands.ExtensionError as e:
            await ctx.send('Invalid extension')

    @commands.is_owner()
    @commands.command(hidden=True)
    async def get_guilds(self, ctx):
        guilds = self.bot.guilds
        await ctx.author.send([guild.name for guild in guilds])

    @commands.is_owner()
    @commands.command(hidden=True)
    async def get_cogs(self, ctx):
        cogs = self.bot.cogs
        await ctx.author.send([str(cog) for cog in cogs])

    @commands.is_owner()
    @commands.command(hidden=True)
    async def get_commands(self, ctx):
        cmds = self.bot.commands
        await ctx.author.send([str(command) for command in cmds])

    @commands.is_owner()
    @commands.command(hidden=True)
    async def get_extensions(self, ctx):
        extensions = self.bot.extensions
        await ctx.author.send([str(extension) for extension in extensions])

    @commands.is_owner()
    @commands.command(hidden=True)
    async def get_latency(self, ctx):
        latency = self.bot.latency
        await ctx.author.send(str(latency))


def setup(bot):
    bot.add_cog(Admin(bot))
