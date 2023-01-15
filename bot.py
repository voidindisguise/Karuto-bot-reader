import requests

from discord.ext import commands

class DiscordClient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=':')
        self.session = requests.Session()
        self.remove_command('help')
    
    async def on_ready(self):
        print("Hello")
    
    async def on_message(self, message):
        if message.author.id != self.user.id:
            await message.channel.send("Hello")


    