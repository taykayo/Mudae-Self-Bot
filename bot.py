import discord
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
token = config['UserInfo']['token']

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as user {client.user}')

@client.event
async def on_message(message):
    # if message.author != client.user:
    #     return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(token)
