from time import sleep

import discord
import configparser

from discord import SlashCommand
from discord.ext.commands import command

config = configparser.ConfigParser()
config.read('config.ini')
token = config['UserInfo']['token']
channel_id = int(config['ServerInfo']['channel_ID'])

client = discord.Client(request_guilds = False)
mudae_channel = None
command_dict = {}

@client.event
async def on_ready():
    print(f'Logged in as user {client.user}')
    mudae_channel = client.get_channel(channel_id)
    print(mudae_channel)
    cmds = await mudae_channel.application_commands()
    for cmd in cmds:
        if cmd.id == 832171928072224789:
            command_dict["Timer"] = cmd
            print(cmd)
    sleep(1)





@client.event
async def on_message(message):
    # if message.author != client.user:
    #     return

    if message.content.startswith('$checktimers'):
        await command_dict["Timer"].__call__(channel=channel_id)


client.run(token)

