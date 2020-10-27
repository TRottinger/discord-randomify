import os

import discord
from dotenv import load_dotenv
from discord_bot_randomizer import randomizer
from discord_bot_randomizer.parse_args import parse_args
from discord_bot_randomizer.parse_args import select_option
from discord_bot_randomizer.bot_help import prepare_help_string, prepare_result_string

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()


@client.event
async def on_ready():
    guild = client.get_guild(int(GUILD))
    print(str(client.user) + ' is currently in guild: ' + str(guild.name))


@client.event
async def on_message(message):
    if message.content.startswith('!rt'):
        channel_selected = message.channel
        author_selected = message.author.mention
        opt, params = select_option(message.content, '!rt')
        # args = parse_args(message.content)
        # print('Receiving request from ' + str(author_selected) + ' in server ' + str(message.guild))

        if opt == 'help':
            return_string = prepare_help_string()
            await channel_selected.send(author_selected + ': ' + return_string)
        elif opt == 'random' or opt == 'no_opt':
            if opt == 'no_opt':
                await channel_selected.send('No option selected. Defaulting to random. Use !rt help to see options.')
            streamer, viewers, game = randomizer.get_random_twitch_stream()
            return_string = prepare_result_string(author_selected, streamer, game, viewers)
            await channel_selected.send(return_string)
        elif opt == 'game':
            game_to_find = params
            streamer, viewers, game = randomizer.get_random_twitch_stream_by_game(game_to_find)
            if streamer is None:
                await channel_selected.send(author_selected + ': Could not find a streamer under game: ' + game_to_find)
            else:
                return_string = prepare_result_string(author_selected, streamer, game, viewers)
                await channel_selected.send(return_string)
        elif opt == 'bad_opt':
            await channel_selected.send(author_selected + ': Oops! I got a bad option. Type !rt help and try again :)')
        else:
            await channel_selected.send(author_selected + ': Oops! I got a bad option. Type !rt help and try again :)')


client.run(TOKEN)
