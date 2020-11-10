import os

from discord.ext import commands
import random

from dotenv import load_dotenv

from utils import http_helpers


class MiscFunctions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        load_dotenv()
        self.cat_api_key = os.getenv('CAT_API_KEY')

    @commands.command(name='repeat', description='Repeat your last run command')
    async def repeat(self, ctx):
        """
        Repeats your last run command
        This is based off the user's last run command, not the bot's
        """
        author = str(ctx.author)
        last_ctx = self.bot.repeat_dict.get(author)
        if last_ctx is not None:
            await last_ctx.reinvoke()
        else:
            await ctx.send(ctx.author.mention + ' please run a command first')

    @commands.command(name='time', description='Get a random time')
    async def time(self, ctx):
        """
        Gets a random time and outputs it to the user. Format is 24 hour clock.
        """
        hour = f'{random.randint(0, 23):02}'
        minute = f'{random.randint(0, 59):02}'
        time = str(hour) + ':' + str(minute)
        await ctx.send(ctx.author.mention + ' ' + time)

    @commands.command(name='emoji', description='Get a random emoji from your server')
    @commands.guild_only()
    async def emoji(self, ctx):
        """
        Selects a random emoji that the bot has access to and outputs it to the channel
        """
        # emojis = self.bot.emojis
        # emoji_choice = random.choice(emojis)
        # await ctx.send(str(emoji_choice))

        # Changing to only be from current guild for safety reasons
        emojis = ctx.guild.emojis
        if len(emojis) == 0:
            await ctx.send('There are no custom emojis for this server')
        else:
            emoji_choice = random.choice(emojis)
            await ctx.send(str(emoji_choice))

    # @commands.command(name='emojis', description='Get some random emojis this bot has access to',
    #                  brief='Emojis. Defaults to 5')
    # async def emojis(self, ctx, *, arg=5):
    #    """
    #    Selects a certain amount of emojis that the bot has access to and outputs them to the channel
    #    The bot will output it in an embedded message
    #    An argument for the number of emojis can be passed in. Default 5. Max 20
    #    Example: emojis 10
    #    :param ctx:
    #    :param arg:
    #    :return:
    #    """
        #if arg > 20:
        #    await ctx.send(ctx.author.mention + ' too many emojis requested.')
        #else:
        #    emojis = self.bot.emojis
        #    emoji_choices = random.sample(emojis, k=arg)
        #    embed = discord.Embed(title='Emojis')
        #    for emoji in emoji_choices:
        #        embed.add_field(name=str(emoji.name), value=str(emoji))
        #    await ctx.send(embed=embed)
    @commands.command(name='dog', description='Get a random doggo picture!', brief="Random dog!")
    async def dog(self, ctx):
        """
        Uses the dog.ceo/dog-api endpoint to get a random doggo!
        """
        response = http_helpers.send_get_request('https://dog.ceo/api/breeds/image/random', headers=None)
        if http_helpers.handle_status_code(response) == 'OK':
            result = response.json()['message']
        else:
            result = 'Sorry, I had trouble finding a dog'
        await ctx.send(str(result))

    @commands.command(name='cat', description='Get a random cat picture!', brief='Random cat!')
    async def cat(self, ctx):
        """
        Uses the cataas.com endpoint to get a random cat
        """
        headers = {
            'x-api-key': self.cat_api_key
        }
        response = http_helpers.send_get_request('https://api.thecatapi.com/v1/images/search', headers=headers)
        if http_helpers.handle_status_code(response) == 'OK':
            result = random.choice(response.json())
            result = result['url']
        else:
            result = 'Sorry, I had trouble finding a cat'

        await ctx.send(str(result))

    @commands.command(name='query', description='Get a random query word', brief='Random query word')
    async def query(self, ctx):
        """
        Gets a random query and outputs it
        """
        choice = self.bot.random_words.get_random_query()
        await ctx.send(ctx.author.mention + ' you got: ' + choice)


def setup(bot):
    bot.add_cog(MiscFunctions(bot))
