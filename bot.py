#!/usr/bin/python3
import asyncio
import os
from math import ceil

import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import pymongo

# Load twitch client id and secret into file
load_dotenv()
TESTING = os.getenv('testing')

if TESTING == 'True':
    TOKEN = os.getenv('TEST_DISCORD_TOKEN')
else:
    TOKEN = os.getenv('DISCORD_TOKEN')

MONGO_DB_URL = os.getenv('MONGO_DB')

SHARED_SERVER = 773783340763316224


class CommandHelpEntry:
    def __init__(self, name, usage, desc):
        self.name = name
        self.usage = usage
        self.desc = desc


class CustomHelpCommand(commands.DefaultHelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        commands_listing = self.context.bot.commands
        help_commands = await self.filter_commands(commands_listing, sort=True)
        inline = False
        # If the message was spawned from a DM, let's not go through the trouble of paginating
        if self.context.guild is None:
            embed = discord.Embed(title='Command Listings')
            embed.colour = discord.Colour.blue()
            embed.description = '''
            List of commands available for Randomify
            For a more user-friendly list of help commands, visit:
            https://trottinger.github.io/discord-randomify/commands
            '''
            embed.set_author(name='Randomify Help Page')
            embed.set_thumbnail(url=self.context.bot.user.avatar_url)
            embed.set_footer(text='Thanks for using Randomify!')
            for command in help_commands:
                if command.usage is not None:
                    embed.add_field(name=str(command.name) + ' ' + str(command.usage), value=str(command.short_doc),
                                    inline=inline)
                else:
                    embed.add_field(name=str(command.name), value=str(command.short_doc), inline=inline)

            await self.context.send(embed=embed)
        else:
            commands_to_paginate = []
            for command in help_commands:
                command_help_entry = CommandHelpEntry(command.name, command.usage, str(command.short_doc))
                commands_to_paginate.append(command_help_entry)
            await self.paginate_help(commands_to_paginate)

    async def paginate_help(self, command_listing):
        bot = self.context.bot
        content = []
        pages = ceil(len(command_listing) / 10)
        for i in range(0, pages):
            embed = discord.Embed(title='Randomify Commands')
            embed.colour = discord.Colour.purple()
            embed.set_thumbnail(url=self.context.bot.user.avatar_url)
            embed.description = '''
            Thank you for using Randomify, the bot for all your random needs!
            List of commands available for Randomify
            For a more user-friendly list of help commands, visit: 
            https://trottinger.github.io/discord-randomify/commands
            
            All commands can be invoked with !rt <command>.
            To set a custom prefix, try: !rt help prefix
            
            Page {page}/{pages}
            '''.format(page=str(i+1), pages=str(pages))
            for j in range(0, 10):
                if (i*10) + j == len(command_listing):
                    break
                curr_command = command_listing[(i*10) + j]
                if curr_command.usage is not None:
                    embed.add_field(name=str(curr_command.name) + ' ' + str(curr_command.usage),
                                    value=str(curr_command.desc),
                                    inline=False)
                else:
                    embed.add_field(name=str(curr_command.name), value=str(curr_command.desc),
                                    inline=False)
            content.append(embed)

        cur_page = 1
        message = await self.context.send(embed=content[cur_page - 1])
        # getting the message object for editing and reacting

        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        def check(reaction, user):
            return user == self.context.author and str(reaction.emoji) in ["◀️", "▶️"]
            # This makes sure nobody except the command sender can interact with the "menu"

        while True:
            try:
                reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check)
                # waiting for a reaction to be added - times out after x seconds, 60 in this
                # example

                if str(reaction.emoji) == "▶️" and cur_page != pages:
                    cur_page += 1
                    await message.edit(embed=content[cur_page - 1])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀️" and cur_page > 1:
                    cur_page -= 1
                    await message.edit(embed=content[cur_page - 1])
                    await message.remove_reaction(reaction, user)

                else:
                    await message.remove_reaction(reaction, user)
                    # removes reactions if the user tries to go forward on the last page or
                    # backwards on the first page
            except asyncio.TimeoutError:
                await message.delete()
                break
                # ending the loop if user doesn't react after x seconds
            except discord.Forbidden:
                print('Invalid perms')
                break


class Bot(commands.AutoShardedBot):
    """
    The main Bot class for Randomify
    """

    def __init__(self, **options):
        super().__init__(**options)
        self.db_client = pymongo.MongoClient(MONGO_DB_URL)
        self.db_bot = self.db_client.get_database('Bot')
        self.db_prefix_table = self.db_bot.get_collection('GuildPrefixes')
        self.default_prefix = '!rt '
        self.repeat_dict = {}
        self.support_id = SHARED_SERVER
        self.help_command = CustomHelpCommand()

    def setup_extensions(self):
        """
        Loads the extensions for the bot
        :return:
        """
        self.load_extension('cogs.config')
        self.load_extension('cogs.misc')
        self.load_extension('cogs.twitch')
        self.load_extension('cogs.reddit')
        self.load_extension('cogs.wiki')
        self.load_extension('cogs.common_randomizers')
        self.load_extension('cogs.games')
        # self.load_extension('cogs.youtube')
        self.load_extension('cogs.anime')
        self.load_extension('cogs.admin')

    def startup(self):
        self.run(TOKEN, reconnect=True)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(ctx.author.mention + '- Sorry, that command does not exist!')

    async def on_guild_join(self, guild):
        channel = self.get_guild(self.support_id).text_channels[0]
        await channel.send('GUILD ADDED ALERT: ' + str(guild) + '. Large guild?: ' + str(guild.large))

    async def on_guild_remove(self, guild):
        channel = self.get_guild(self.support_id).text_channels[0]
        await channel.send('GUILD REMOVED ALERT: ' + str(guild) + '. Large guild?: ' + str(guild.large))

    async def on_command_completion(self, ctx):
        # add to repeat dict if not 'repeat' called
        str_command = str(ctx.command)
        if str_command != 'repeat':
            self.repeat_dict[str(ctx.message.author)] = ctx

    async def set_guild_prefix(self, guild, prefix):
        if prefix == '':
            res = 'Empty prefix'
        elif prefix.isspace():
            res = 'Badly formed prefix'
        else:
            entry = {
                'Guild': guild,
                'Prefix': prefix
            }
            self.db_prefix_table.find_one_and_update({'Guild': guild}, {"$set": entry}, upsert=True)
            res = ''
        return res

    def get_guild_prefix(self, guild):
        entry = self.db_prefix_table.find_one({'Guild': guild})

        if entry is None:
            prefix = self.default_prefix
        else:
            prefix = str(entry['Prefix'])
        return prefix

    async def get_guilds(self):
        return self.guilds
