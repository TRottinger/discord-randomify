import random

from discord.ext import commands

CHAMPS = ['Aatrox', 'Ahri', 'Akali', 'Alistar', 'Amumu', 'Anivia', 'Annie', 'Aphelios', 'Ashe', 'Azir', 'Bard',
          'Blitzcrank', 'Brand', 'Caitlyn', 'Camille', 'Cassiopeia', 'Chogath', 'Corki', 'Darius', 'Diana', 'Draven',
          'DrMundo', 'Ekko', 'Elise', 'Evelynn', 'Ezreal', 'Fiora', 'Fizz', 'Gangplank', 'Garen', 'Gnar', 'Gragas',
          'Graves', 'Heimerdinger', 'Irelia', 'Ivern', 'Janna', 'JarvanIV', 'Jax', 'Jayce', 'Jhin', 'Jinx', 'Kaisa',
          'Kalista', 'Karma', 'Karthus', 'Kassadin', 'Katarina', 'Kayle', 'Kayn', 'Kennen', 'Khazix', 'Kled', 'KogMaw',
          'Leblanc', 'LeeSin', 'Leona', 'Lillia', 'Lissandra', 'Lucian', 'Lulu', 'Lux', 'Malzahar', 'Maokai',
          'MasterYi', 'MissFortune', 'MonkeyKing', 'Mordekaiser', 'Morgana', 'Nami', 'Nasus', 'Neeko', 'Nidalee',
          'Nocturne', 'Nunu', 'Orianna', 'Ornn', 'Pantheon', 'Poppy', 'Pyke', 'Qiyana', 'Quinn', 'Rakan', 'Rammus',
          'RekSai', 'Renekton', 'Riven', 'Rumble', 'Samira', 'Sejuani', 'Senna', 'Shaco', 'Shen', 'Sion', 'Sivir',
          'Skarner', 'Sona', 'Soraka', 'Sylas', 'Syndra', 'TahmKench', 'Taliyah', 'Talon', 'Taric', 'Teemo', 'Thresh',
          'Tristana', 'Trundle', 'TwistedFate', 'Twitch', 'Urgot', 'Varus', 'Vayne', 'Veigar', 'Velkoz', 'Viktor',
          'Vladimir', 'Xayah', 'Xerath', 'XinZhao', 'Yasuo', 'Yone', 'Yorick', 'Yuumi', 'Zac', 'Zilean', 'Zoe']

SUMMONER_SPELLS = ['Heal', 'Ghost', 'Barrier', 'Exhaust', 'Flash', 'Teleport', 'Smite', 'Cleanse', 'Ignite']
SUMMONER_SPELLS_ARAM = ['Heal', 'Ghost', 'Barrier', 'Exhaust', 'Flash', 'Clarity', 'Snowball', 'Cleanse', 'Ignite']


class LeagueOfLegends(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="champion", description="Get a random League of Legends champion",
                      brief="Get a random League Champion")
    async def champion(self, ctx):
        champion = random.choice(CHAMPS)
        author = ctx.author.mention
        await ctx.send(author + ' You got ' + champion + '!')

    @commands.command(name="summoner_spell", description="Get a random League of Legends summoner spell",
                      brief="Get a random League summoner spell")
    async def summoner_spell(self, ctx):
        ss = random.choice(SUMMONER_SPELLS)
        author = ctx.author.mention
        await ctx.send(author + ' You got ' + ss + '!')

    @commands.command(name="champ_select", description="Get a random champion and 2 summoner spells",
                      brief="Get a random champ + 2 summoners")
    async def champ_select(self, ctx):
        champion = random.choice(CHAMPS)
        ss = random.sample(SUMMONER_SPELLS, k=2)
        author = ctx.author.mention
        await ctx.send(author + ' You got ' + champion + ' with ' + ss[0] + ' and ' + ss[1] + '!')

    @commands.command(name="summoner_spell_aram", description="Get a random League of Legends ARAM summoner spell",
                      brief="Get a random League ARAM summoner spell")
    async def summoner_spell_aram(self, ctx):
        ss = random.choice(SUMMONER_SPELLS_ARAM)
        author = ctx.author.mention
        await ctx.send(author + ' You got ' + ss + '!')

    @commands.command(name="champ_select_aram", description="Get 2 summoner spells for ARAM",
                      brief="Get 2 ARAM summoners")
    async def champ_select_aram(self, ctx):
        ss = random.sample(SUMMONER_SPELLS_ARAM, k=2)
        author = ctx.author.mention
        await ctx.send(author + ' You got ' + ss[0] + ' and ' + ss[1] + '!')

    @commands.command(name="aram_reroll", description="Get Y/N value on whether you should reroll",
                      brief="Get reroll Y/N")
    async def aram_reroll(self, ctx):
        choice = random.choice(['Yes', 'No'])
        author = ctx.author.mention
        await ctx.send(author + ' Reroll: ' + choice)


def setup(bot):
    bot.add_cog(LeagueOfLegends(bot))
