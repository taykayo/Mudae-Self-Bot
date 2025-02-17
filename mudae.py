import json
import configparser
from time import sleep
import datetime
import requests
import re
1340809637821157398
config = configparser.ConfigParser()
config.read('config.ini')
channel_id = int(config['ServerInfo']['channel_ID'])
user_token = config['UserInfo']['token']
user_ID = config['UserInfo']['user_ID']
url = f'https://discord.com/api/v10/channels/{channel_id}/messages'
test_url = f'https://discord.com/api/v10/channels/{channel_id}/messages?around=1340809637821157398'

key_emoji='🔑'
kaka_emoji='💎'
claimed_emoji ='🤍'
owned_emoji ='⭐'
unclaimed_emoji ='❌'
roll_history = ['No History']

def test_get_char_object():
    messages_req = requests.get(test_url, headers={'authorization': user_token})
    messages_jsons = json.loads(messages_req.text)
    print(messages_jsons)
    # for message in messages_jsons:
    #     if message['interaction']['user']['id'] == user_ID:
    #         char_card = message
    #         print(char_card)
    #         return MudaeCharacter(ctx, char_card)

def get_char_object(ctx):
    messages_req = requests.get(url, headers={'authorization': user_token})
    messages_jsons = json.loads(messages_req.text)
    for message in messages_jsons:
        if message['interaction']['user']['id'] == user_ID:
            char_card = message
            print(char_card)
            return MudaeCharacter(ctx, char_card)

class MudaeCharacter:
    def __init__(self, ctx, char_card):
        self.char_name = char_card['embeds'][0]['author']['name']
        self.char_show =re.search("(^[^<|(\\n)]*)", char_card['embeds'][0]['description']).group()
        self.kaka_value = re.search("(\\*\\*\\d*\\*\\*)", char_card['embeds'][0]['description']).group()[2:-2]
        self.claim_status = "Belongs to" in char_card['embeds'][0]['footer']['text']
        if self.claim_status:
            if str(ctx.author) in char_card['embeds'][0]['footer']['text']:
                self.owner_emoji = owned_emoji
            else:
                self.owner_emoji = claimed_emoji
        else:
            self.owner_emoji = unclaimed_emoji

        try:
            key_num = re.search("\\(.*(\\d).*\\)", char_card['embeds'][0]['description']).group()[1:-1]
            self.key_string = f" - {key_num}{key_emoji}"
        except AttributeError:
            self.key_string = ""
            pass

    def __str__(self):
        return f'{self.owner_emoji}{self.key_string} - {self.kaka_value}{kaka_emoji}  -  {self.char_name}  |  {self.char_show}'


class MudaeCommander:
    def __init__(self, command_dict, mudae_channel):
        self.command_dict = command_dict
        self.mudae_channel = mudae_channel

    async def send_timer(self):
        await self.command_dict["tu"].__call__(channel=self.mudae_channel.id)

    def beautify_roll(self):
        return


    async def send_im(self, ctx, char_name:str):
        await self.command_dict["im"].__call__(channel=self.mudae_channel.id, input=char_name)
        print(get_char_object(ctx))


    async def send_rolls(self, ctx, category, amount:int):
        global roll_history
        if roll_history[0] == "No History":
            roll_history = []
        rolls = []
        roll_start_time = datetime.datetime.now()
        for i in range(amount):
            await self.command_dict[f"{category}"].__call__(channel=self.mudae_channel.id)
            rolls.append(f'{str(i+1)} - {get_char_object(ctx)}')
            sleep(2)

        roll_string = f"Rolls at {roll_start_time}\n{'\n'.join(rolls)}"
        roll_history.append(roll_string)
        return

    async def check_roll_history(self):
        for i in range(0,len(roll_history),3):
            try:
                await self.mudae_channel.send(f"{'\n\n'.join(roll_history[i:i+3])}\n")
            except:
                raise

        return

    async def clear_roll_history(self):
        global roll_history
        roll_history = ['No History']
        await self.mudae_channel.send("Roll history has been cleared")


