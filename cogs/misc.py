from discord.ext import commands
import discord
import random


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

    @commands.command(name='time', description='Get a random time',
                      brief='Get a random time')
    async def time(self, ctx):
        hour = f'{random.randint(0, 23):02}'
        minute = f'{random.randint(0, 59):02}'
        time = str(hour) + ':' + str(minute)
        await ctx.send(ctx.author.mention + ' ' + time)

    @commands.command(name='emoji', description='Get a random emoji this bot has access to',
                      brief='Emoji')
    async def emoji(self, ctx):
        emojis = self.bot.emojis
        emoji_choice = random.choice(emojis)
        await ctx.send(str(emoji_choice))

    @commands.command(name='emojis', description='Get some random emojis this bot has access to',
                      brief='Emojis. Defaults to 5')
    async def emojis(self, ctx, *, arg=5):
        if arg > 20:
            await ctx.send(ctx.author.mention + ' too many emojis requested.')
        else:
            emojis = self.bot.emojis
            emoji_choices = random.sample(emojis, k=arg)
            embed = discord.Embed(title='Emojis')
            for emoji in emoji_choices:
                embed.add_field(name=str(emoji.name), value=str(emoji))
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(MiscFunctions(bot))
