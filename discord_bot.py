import os

import discord
from dotenv import load_dotenv
import randomizer
from parse_args import parse_args

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
    if '.randomTwitch' in message.content or '.rt' in message.content:
        channel_selected = message.channel
        author_selected = message.author.mention
        args = parse_args(message.content)
        streamer, viewers, game, res_string = randomizer.get_random_twitch_stream_with_args(args)
        if res_string != '':
            await channel_selected.send(author_selected + ': ' + res_string)
        else:
            await channel_selected.send(
                author_selected + ' - You got ' + streamer + ' playing ' + game + ' with a viewer count of ' + viewers)
            await channel_selected.send('https://twitch.tv/' + streamer)


client.run(TOKEN)
