from discord.ext import commands


class MiscFunctions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='repeat', description='Repeat your last run command',
                      brief='Repeat your command')
    async def repeat(self, ctx):
        author = str(ctx.author)
        last_ctx = self.bot.repeat_dict.get(author)
        if last_ctx is not None:
            await last_ctx.reinvoke()
        else:
            await ctx.send(ctx.author.mention + ' please run a command first')


def setup(bot):
    bot.add_cog(MiscFunctions(bot))
