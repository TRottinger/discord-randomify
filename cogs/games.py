import os
import random

from discord.ext import commands
from dotenv import load_dotenv

from utils.http_helpers import get_access_token, form_auth_headers, send_get_request


class LeagueOfLegends:
    def __init__(self):
        self.champs = ['Aatrox', 'Ahri', 'Akali', 'Alistar', 'Amumu', 'Anivia', 'Annie', 'Aphelios', 'Ashe', 'Azir',
                       'Bard', 'Blitzcrank', 'Brand', 'Caitlyn', 'Camille', 'Cassiopeia', 'Chogath', 'Corki',
                       'Darius', 'Diana', 'Draven', 'DrMundo', 'Ekko', 'Elise', 'Evelynn', 'Ezreal',
                       'Fiora', 'Fizz', 'Gangplank', 'Garen', 'Gnar', 'Gragas', 'Graves', 'Heimerdinger', 'Irelia',
                       'Ivern', 'Janna', 'JarvanIV', 'Jax', 'Jayce', 'Jhin', 'Jinx', 'Kaisa', 'Kalista', 'Karma',
                       'Karthus', 'Kassadin', 'Katarina', 'Kayle', 'Kayn', 'Kennen', 'Khazix',
                       'Kled', 'KogMaw', 'Leblanc', 'LeeSin', 'Leona', 'Lillia', 'Lissandra', 'Lucian',
                       'Lulu', 'Lux', 'Malzahar', 'Maokai', 'MasterYi', 'MissFortune', 'MonkeyKing',
                       'Mordekaiser', 'Morgana', 'Nami', 'Nasus', 'Neeko', 'Nidalee', 'Nocturne', 'Nunu', 'Orianna',
                       'Ornn', 'Pantheon', 'Poppy', 'Pyke', 'Qiyana', 'Quinn', 'Rakan', 'Rammus',
                       'RekSai', 'Renekton', 'Riven', 'Rumble', 'Samira', 'Sejuani', 'Senna', 'Shaco', 'Shen', 'Sion',
                       'Sivir', 'Skarner', 'Sona', 'Soraka', 'Sylas', 'Syndra', 'TahmKench', 'Taliyah', 'Talon',
                       'Taric', 'Teemo', 'Thresh', 'Tristana', 'Trundle', 'TwistedFate', 'Twitch', 'Urgot', 'Varus',
                       'Vayne', 'Veigar', 'Velkoz', 'Viktor', 'Vladimir', 'Xayah', 'Xerath', 'XinZhao', 'Yasuo',
                       'Yone', 'Yorick', 'Yuumi', 'Zac', 'Zilean', 'Zoe']

        self.summoner_spells = ['Heal', 'Ghost', 'Barrier', 'Exhaust', 'Flash',
                                'Teleport', 'Smite', 'Cleanse', 'Ignite']

        self.summoner_spells_aram = ['Heal', 'Ghost', 'Barrier', 'Exhaust', 'Flash',
                                     'Clarity', 'Snowball', 'Cleanse', 'Ignite']

    async def champion(self, ctx):
        champion = random.choice(self.champs)
        author = ctx.author.mention
        await ctx.send(author + ' You got ' + champion + '!')

    async def summoner_spell(self, ctx):
        ss = random.choice(self.summoner_spells)
        author = ctx.author.mention
        await ctx.send(author + ' You got ' + ss + '!')

    async def champ_select(self, ctx):
        champion = random.choice(self.champs)
        ss = random.sample(self.summoner_spells, k=2)
        author = ctx.author.mention
        await ctx.send(author + ' You got ' + champion + ' with ' + ss[0] + ' and ' + ss[1] + '!')

    async def summoner_spell_aram(self, ctx):
        ss = random.choice(self.summoner_spells_aram)
        author = ctx.author.mention
        await ctx.send(author + ' You got ' + ss + '!')

    async def champ_select_aram(self, ctx):
        ss = random.sample(self.summoner_spells_aram, k=2)
        author = ctx.author.mention
        await ctx.send(author + ' You got ' + ss[0] + ' and ' + ss[1] + '!')

    async def aram_reroll(self, ctx):
        choice = random.choice(['Yes', 'No'])
        author = ctx.author.mention
        await ctx.send(author + ' Reroll: ' + choice)


class WorldOfWarcraft:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv('BLIZZARD_CLIENT_ID')
        self.client_secret = os.getenv('BLIZZARD_CLIENT_SECRET')
        self.client_auth = get_access_token(self.client_id, self.client_secret, 'https://us.battle.net/oauth/token')
        self.auth_headers = form_auth_headers(self.client_id, self.client_auth)


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.league_handler = LeagueOfLegends()
        self.wow_handler = WorldOfWarcraft()

    # League of Legends commands

    @commands.command(name="champion", description="Get a random League of Legends champion",
                      brief="Get a random League Champion")
    async def champion(self, ctx):
        await self.league_handler.champion(ctx)

    @commands.command(name="summonerspell", description="Get a random League of Legends summoner spell",
                      brief="Get a random League summoner spell")
    async def summoner_spell(self, ctx):
        await self.league_handler.summoner_spell(ctx)

    @commands.command(name="champselect", description="Get a random champion and 2 summoner spells",
                      brief="Get a random champ + 2 summoners")
    async def champ_select(self, ctx):
        await self.league_handler.champ_select(ctx)

    @commands.command(name="summonerspellaram", description="Get a random League of Legends ARAM summoner spell",
                      brief="Get a random League ARAM summoner spell")
    async def summoner_spell_aram(self, ctx):
        await self.league_handler.summoner_spell_aram(ctx)

    @commands.command(name="champselectaram", description="Get 2 summoner spells for ARAM",
                      brief="Get 2 ARAM summoners")
    async def champ_select_aram(self, ctx):
        await self.league_handler.champ_select_aram(ctx)

    @commands.command(name="aramreroll", description="Get Y/N value on whether you should reroll",
                      brief="Get reroll Y/N")
    async def aram_reroll(self, ctx):
        await self.league_handler.aram_reroll(ctx)

    # End League of Legends commands


def setup(bot):
    bot.add_cog(Games(bot))
