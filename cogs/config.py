from discord.ext import commands


class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def ping(self, ctx):
        await ctx.send('Pong')

    @commands.command(name='prefix', description='Set the prefix for this guild',
                      brief='Set prefix for invocation', aliases=['prefix_set'])
    @commands.guild_only()
    async def prefix(self, ctx, prefix):
        ret = await self.bot.set_guild_prefix(ctx.guild.id, prefix)
        if ret == '':
            await ctx.send('The prefix has been set to ' + str(prefix))
        else:
            await ctx.send('Invalid prefix. Sorry :(')

    @commands.command(name='get_prefix', description='Get the prefix for this guild',
                      brief='Get prefix for invocation', aliases=['prefix_get'])
    @commands.guild_only()
    async def get_prefix(self, ctx):
        prefix = self.bot.get_guild_prefix(ctx.guild.id)
        author = ctx.author.mention
        if self.bot.default_prefix == prefix:
            await ctx.send(author + ' available prefixes are: \"' + self.bot.default_prefix + '\"')
        else:
            await ctx.send(author + ' available prefixes are: \"' + self.bot.default_prefix + '\" and \"'
                           + prefix + '\"')


def setup(bot):
    bot.add_cog(Config(bot))
