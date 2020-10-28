import os

import discord
from dotenv import load_dotenv
from discord_bot_randomizer import randomizer
import random
from discord_bot_randomizer.parse_args import parse_args
from discord_bot_randomizer.parse_args import select_option
from discord_bot_randomizer.bot_help import prepare_help_string, prepare_result_string
from discord_bot_randomizer.common_randomizers import flip_coin
from discord_bot_randomizer.common_randomizers import roll_dice

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
        print('Running in channel: ' + str(channel_selected))
        print('Running in server: ' + str(message.guild))
        print('Running for author: ' + str(message.author))
        print('Running with opt: ' + str(opt))
        print('Running with params: ' + str(params))
        # args = parse_args(message.content)
        # print('Receiving request from ' + str(author_selected) + ' in server ' + str(message.guild))

        # TODO: Let's clean this up into something more manageable and scalable
        # TODO: Change twitch stream output to be a data type (i.e. struct)
        if opt == 'help':
            return_string = prepare_help_string()
            await channel_selected.send(author_selected + ': ' + return_string)

        elif opt == 'coinflip':
            result = flip_coin()
            await channel_selected.send(author_selected + ' ' + result + '!')

        elif opt == 'diceroll':
            result = roll_dice()
            await channel_selected.send(author_selected + ' ' + str(result) + '!')

        elif opt == 'wiki':
            result = randomizer.get_random_wiki_article()
            await channel_selected.send(author_selected + ' ' + str(result) + '')

        elif opt == 'reddit':
            result = randomizer.get_random_subreddit()
            await channel_selected.send(author_selected + ' ' + str(result) + '')

        elif opt == 'streamer':
            result = randomizer.get_random_twitch_stream()
            # Make common data type for this
            return_string = prepare_result_string(author_selected, result[0], result[2], result[1])
            await channel_selected.send(return_string)

        elif opt == 'random' or opt == 'no_opt':
            if opt == 'no_opt':
                await channel_selected.send('No option selected. Defaulting to random. Use !rt help to see options.')
            links = ['reddit', 'wiki', 'streamer']
            result = random.choice(links)
            if result == 'streamer':
                result = randomizer.get_random_twitch_stream()
                # Make common data type for this
                return_string = prepare_result_string(author_selected, result[0], result[2], result[1])
                await channel_selected.send(return_string)
            elif result == 'wiki':
                result = randomizer.get_random_wiki_article()
                await channel_selected.send(author_selected + ' ' + str(result) + '')
            elif result == 'reddit':
                result = randomizer.get_random_subreddit()
                await channel_selected.send(author_selected + ' ' + str(result) + '')
            else:
                await channel_selected.send(author_selected + ' something went wrong :(')

        elif opt == 'game':
            game_to_find = params
            result = randomizer.get_random_twitch_stream_by_game(game_to_find)
            if result[0] is None:
                await channel_selected.send(author_selected + ': Could not find a streamer under game: ' + game_to_find)
            else:
                return_string = prepare_result_string(author_selected, result[0], result[2], result[1])
                await channel_selected.send(return_string)

        elif opt == 'bad_opt':
            await channel_selected.send(author_selected + ': Oops! I got a bad option. Type !rt help and try again :)')

        else:
            await channel_selected.send(author_selected + ': Oops! I got a bad option. Type !rt help and try again :)')


client.run(TOKEN)
