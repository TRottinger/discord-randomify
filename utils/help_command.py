import asyncio
from math import ceil

import discord
from discord.ext import commands


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
        if self.context.guild is not None:
            manage_messages = self.context.channel.permissions_for(self.context.guild.me).manage_messages
            add_reactions = self.context.channel.permissions_for(self.context.guild.me).add_reactions
            print(str(manage_messages))
            print(str(add_reactions))
        else:
            manage_messages = False
            add_reactions = False
        if manage_messages is True and add_reactions is True:
            commands_to_paginate = []
            for command in help_commands:
                command_help_entry = CommandHelpEntry(command.name, command.usage, str(command.short_doc))
                commands_to_paginate.append(command_help_entry)
            await self.paginate_help(commands_to_paginate)
        else:
            embed = discord.Embed(title='Randomify Commands')
            embed.colour = discord.Colour.blue()
            embed.description = '''
                        List of commands available for Randomify
                        For a more user-friendly list of help commands, visit:
                        https://trottinger.github.io/discord-randomify/commands
                        '''
            embed.set_author(name='Randomify Help Page')
            embed.set_thumbnail(url=self.context.bot.user.avatar_url)
            embed.set_footer(text='Thanks for using Randomify! Review and upvote at https://top.gg/bot/770197604155785216')
            for command in help_commands:
                if command.usage is not None:
                    embed.add_field(name=str(command.name) + ' ' + str(command.usage), value=str(command.short_doc),
                                    inline=inline)
                else:
                    embed.add_field(name=str(command.name), value=str(command.short_doc), inline=inline)

                if len(embed.fields) == 20:
                    await self.context.author.send(embed=embed)
                    embed.clear_fields()

            await self.context.author.send(embed=embed)

    # Credit Diggy on Stack Overflow: https://stackoverflow.com/a/61793587
    async def paginate_help(self, command_listing):
        bot = self.context.bot
        content = []
        pages = ceil(len(command_listing) / 10)
        for i in range(0, pages):
            embed = discord.Embed(title='Randomify Commands')
            embed.colour = discord.Colour.purple()
            embed.set_thumbnail(url=self.context.bot.user.avatar_url)
            embed.set_footer(text='Review and upvote at https://top.gg/bot/770197604155785216')
            embed.description = '''
            Thank you for using Randomify, the bot for all your random needs!
            To review and upvote, visit: https://top.gg/bot/770197604155785216
            For a more user-friendly list of help commands, visit: 
            https://trottinger.github.io/discord-randomify/commands
            To set a custom prefix, try: !rt help prefix
            This message will delete after 60 seconds of inactivity

            Page {page}/{pages}
            '''.format(page=str(i + 1), pages=str(pages))
            for j in range(0, 10):
                if (i * 10) + j == len(command_listing):
                    break
                curr_command = command_listing[(i * 10) + j]
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
        await message.add_reaction("🛑")

        def check(react, usr):
            return usr == self.context.author and str(react.emoji) in ["◀️", "▶️", "🛑"]
            # This makes sure nobody except the command sender can interact with the "menu"

        while True:
            try:
                reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check)
                # waiting for a reaction to be added - times out after x seconds, 60 in this
                # example

                # Spam prevention
                await asyncio.sleep(delay=1)

                if str(reaction.emoji) == "▶️" and cur_page != pages:
                    cur_page += 1
                    await message.edit(embed=content[cur_page - 1])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀️" and cur_page > 1:
                    cur_page -= 1
                    await message.edit(embed=content[cur_page - 1])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "🛑":
                    await message.delete()
                    break

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
