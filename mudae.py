import json
from time import sleep

class MudaeCommander:
    def __init__(self, command_dict, mudae_channel):
        self.command_dict = command_dict
        self.mudae_channel = mudae_channel

    async def send_timer(self):
        await self.command_dict["tu"].__call__(channel=self.mudae_channel.id)

    async def send_rolls(self,category, amount:int):
        for _ in range(amount):
            await self.command_dict[f"{category}"].__call__(channel=self.mudae_channel.id)
            # await self.mudae_channel.send(f'Dummy roll')
            sleep(2)
        return
