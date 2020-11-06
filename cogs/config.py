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

    @prefix.error
    async def prefix_error(self, ctx, error):
        author = ctx.author.mention
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(author + ' - Please provide an argument')

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

    @commands.command(name='github', description='Get the code for the me!',
                      brief='Get my code')
    async def github(self, ctx):
        github = 'https://github.com/TRottinger/discord-randomify'
        author = ctx.author.mention
        await ctx.send(author + ' check out my code on GitHub: ' + github)

    @commands.command(name='discord', description='Invite link to the bot discord',
                      brief='Bot discord', aliases=['git'])
    async def discord(self, ctx):
        discord = 'https://discord.gg/EbZ3QX4'
        author = ctx.author.mention
        await ctx.send(author + ' join our Discord server: ' + discord)

    @commands.command(name='invite', description='Invite link to have bot join your Discord',
                      brief='Invite link for bot')
    async def invite(self, ctx):
        await ctx.send('To invite the bot to your server, use: https://bit.ly/2JqfTQN')


def setup(bot):
    bot.add_cog(Config(bot))
