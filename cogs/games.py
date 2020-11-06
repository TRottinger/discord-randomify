import os
import random

from discord.ext import commands
from dotenv import load_dotenv

from utils.http_helpers import get_access_token, form_auth_headers, send_get_request, handle_status_code


class LeagueOfLegends:
    """
    Class for handling methods related to League of Legends
    """

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
        """
        Send a message with a random champion
        :param ctx:
        :return:
        """
        champion = random.choice(self.champs)
        author = ctx.author.mention
        await ctx.send(author + ' You got ' + champion + '!')

    async def summoner_spell(self, ctx):
        """
        Send a message with a random summoner spell
        :param ctx:
        :return:
        """
        ss = random.choice(self.summoner_spells)
        author = ctx.author.mention
        await ctx.send(author + ' You got ' + ss + '!')

    async def champ_select(self, ctx):
        """
        Send a message with a random champion and two random summoner spells
        Note this is only for Summoner's ift
        :param ctx:
        :return:
        """
        champion = random.choice(self.champs)
        ss = random.sample(self.summoner_spells, k=2)
        author = ctx.author.mention
        await ctx.send(author + ' You got ' + champion + ' with ' + ss[0] + ' and ' + ss[1] + '!')

    async def summoner_spell_aram(self, ctx):
        """
        Send a message with a random ARAM summoner spell
        :param ctx:
        :return:
        """
        ss = random.choice(self.summoner_spells_aram)
        author = ctx.author.mention
        await ctx.send(author + ' You got ' + ss + '!')

    async def champ_select_aram(self, ctx):
        """
        Send a message with two random summoner spells for ARAM
        :param ctx:
        :return:
        """
        ss = random.sample(self.summoner_spells_aram, k=2)
        author = ctx.author.mention
        await ctx.send(author + ' You got ' + ss[0] + ' and ' + ss[1] + '!')

    async def aram_reroll(self, ctx):
        """
        Yes / No message for ARAM reroll
        :param ctx:
        :return:
        """
        choice = random.choice(['Yes', 'No'])
        author = ctx.author.mention
        await ctx.send(author + ' Reroll: ' + choice)


class WorldOfWarcraft:
    """
    Class for handling methods related to World of Warcraft
    """

    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv('BLIZZARD_CLIENT_ID')
        self.client_secret = os.getenv('BLIZZARD_CLIENT_SECRET')
        self.access_token = get_access_token(self.client_id, self.client_secret, 'https://us.battle.net/oauth/token')
        self.auth_headers = form_auth_headers(self.client_id, self.access_token)
        self.blizzard_api_url = 'https://us.api.blizzard.com'
        self.classes = self.get_wow_classes()
        self.races = self.get_wow_races()
        self.achievements = self.get_wow_achievements()

    def get_wow_classes(self):
        """
        Queries the WoW API for a list of playable classes
        :return: classes
        """
        headers = {
            'Battlenet-Namespace': 'static-us',
            'locale': 'en_US',
            'client-id': self.client_id,
            'Authorization': 'Bearer ' + self.access_token
        }
        result = send_get_request(self.blizzard_api_url + '/data/wow/playable-class/index', headers=headers)
        if handle_status_code(result) == 'OK':
            json_classes = result.json()['classes']
            classes = []
            for entry in json_classes:
                classes.append(entry['name']['en_US'])
        else:
            classes = ['Warrior', 'Paladin', 'Hunter', 'Rogue', 'Priest', 'Death Knight', 'Shaman', 'Mage', 'Warlock',
                       'Monk', 'Druid', 'Demon Hunter']
        return classes

    def get_wow_races(self):
        """
        Queries the WoW API for a list of playable races
        :return: races
        """
        headers = {
            'Battlenet-Namespace': 'static-us',
            'locale': 'en_US',
            'client-id': self.client_id,
            'Authorization': 'Bearer ' + self.access_token
        }
        result = send_get_request(self.blizzard_api_url + '/data/wow/playable-race/index', headers=headers)
        if handle_status_code(result) == 'OK':
            json_races = result.json()['races']
            races = []
            for entry in json_races:
                races.append(entry['name']['en_US'])
        else:
            races = []
        return races

    def get_wow_achievements(self):
        """
        Queries the WoW API for a list of playable achievements
        :return: achievements
        """
        headers = {
            'Battlenet-Namespace': 'static-us',
            'locale': 'en_US',
            'client-id': self.client_id,
            'Authorization': 'Bearer ' + self.access_token
        }
        result = send_get_request(self.blizzard_api_url + '/data/wow/achievement/index', headers=headers)
        if handle_status_code(result) == 'OK':
            json_achievements = result.json()['achievements']
            achievements = []
            for achievement in json_achievements:
                achievements.append(achievement['name']['en_US'])
        else:
            achievements = []
        return achievements

    async def get_random_wow_class(self):
        """
        Returns a random wow class
        :return: class
        """
        return random.choice(self.classes)

    async def get_random_wow_race(self):
        """
        Returns a random wow race
        :return: race
        """
        return random.choice(self.races)

    async def get_random_wow_achievement(self):
        """
        Returns a random wow achievement
        :return: achievement
        """
        return random.choice(self.achievements)


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.league_handler = LeagueOfLegends()
        self.wow_handler = WorldOfWarcraft()

    # League of Legends commands

    @commands.command(name="champion", description="Get a random League of Legends champion",
                      brief="Get a random League Champion")
    async def champion(self, ctx):
        """
        Bot command that calls league handler champion()
        :param ctx:
        :return:
        """
        await self.league_handler.champion(ctx)

    @commands.command(name="summonerspell", description="Get a random League of Legends summoner spell",
                      brief="Get a random League summoner spell")
    async def summoner_spell(self, ctx):
        """
        Bot command that calls league handler summoner_spell()
        :param ctx:
        :return:
        """
        await self.league_handler.summoner_spell(ctx)

    @commands.command(name="champselect", description="Get a random champion and 2 summoner spells",
                      brief="Get a random champ + 2 summoners")
    async def champ_select(self, ctx):
        """
        Bot command that calls league handler champ_select()
        :param ctx:
        :return:
        """
        await self.league_handler.champ_select(ctx)

    @commands.command(name="summonerspellaram", description="Get a random League of Legends ARAM summoner spell",
                      brief="Get a random League ARAM summoner spell")
    async def summoner_spell_aram(self, ctx):
        """
        Bot command that calls league handler summoner_spell_aram()
        :param ctx:
        :return:
        """
        await self.league_handler.summoner_spell_aram(ctx)

    @commands.command(name="champselectaram", description="Get 2 summoner spells for ARAM",
                      brief="Get 2 ARAM summoners")
    async def champ_select_aram(self, ctx):
        """
        Bot command that calls league handler champ_select_aram()
        :param ctx:
        :return:
        """
        await self.league_handler.champ_select_aram(ctx)

    @commands.command(name="aramreroll", description="Get Y/N value on whether you should reroll",
                      brief="Get reroll Y/N")
    async def aram_reroll(self, ctx):
        """
        Bot command that calls league handler aram_reroll()
        :param ctx:
        :return:
        """
        await self.league_handler.aram_reroll(ctx)

    # End League of Legends commands
    # ***********************************
    # ***********************************
    # World of Warcraft Commands

    @commands.command(name='wowclass', description='Get a random World of Warcraft class', brief='Random WoW class')
    async def wowclass(self, ctx):
        """
        Bot command that calls wow handler get_random_wow_class() to get a random class
        Then, outputs to the caller
        :param ctx:
        :return:
        """
        choice = await self.wow_handler.get_random_wow_class()
        author = ctx.author.mention
        await ctx.send(author + ' You got ' + choice + '!')

    @commands.command(name='wowrace', description='Get a random World of Warcraft race', brief='Random WoW race')
    async def wowrace(self, ctx):
        """
        Bot command that calls wow handler get_random_wow_race() to get a random race
        Then, outputs to the caller
        :param ctx:
        :return:
        """
        choice = await self.wow_handler.get_random_wow_race()
        author = ctx.author.mention
        await ctx.send(author + ' You got ' + str(choice) + '!')

    @commands.command(name='wowachieve', description='Get a random World of Warcraft achievement',
                      brief='Random WoW achievement')
    async def wowachieve(self, ctx):
        """
        Bot command that calls wow handler get_random_wow_achievement() to get a random achievement
        Then, outputs to the caller
        :param ctx:
        :return:
        """
        choice = await self.wow_handler.get_random_wow_achievement()
        author = ctx.author.mention
        await ctx.send(author + ' You got ' + str(choice))


def setup(bot):
    bot.add_cog(Games(bot))
