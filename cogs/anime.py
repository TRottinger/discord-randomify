
import logging
import random

from discord.ext import commands, tasks
import mal

from utils.common_utils import get_random_query

log = logging.getLogger(__name__)


class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="anime", description="Get a random anime", brief="Get a random anime. SFW")
    async def anime(self, ctx):
        """
        Queries the MAL api with a random word to get an anime
        """
        query_word = get_random_query()
        search = mal.AnimeSearch(query_word + '?nsfw=False')
        if len(search.results) == 0:
            await ctx.send('I had trouble querying MAL')
        else:
            author = ctx.author.mention
            choice = random.choice(search.results)
            await ctx.send(author + ' Check this out on MAL: '
                           + str(choice.url))

    @commands.command(name="manga", description="Get a random manga", brief="Get a random manga. SFW")
    async def manga(self, ctx):
        """
        Queries the MAL api with a random word to get an anime
        """
        query_word = get_random_query()
        search = mal.MangaSearch(query_word + '?nsfw=False')
        if len(search.results) == 0:
            await ctx.send('I had trouble querying MAL')
        else:
            author = ctx.author.mention
            choice = random.choice(search.results)
            await ctx.send(author + ' Check this out on MAL: '
                           + str(choice.url))


def setup(bot):
    bot.add_cog(Anime(bot))
