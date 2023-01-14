import discord, os, run_server, requests

from discord.ext import commands


class disClient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=':')
        self.session = requests.Session()
        self.token = os.getenv("TOKEN")
        self.remove_command('help')

    async def on_message(self, message):
        if message.author.id != 301856154332692480:
            await message.channel.send("Hello")
            

    def getHeaders(self):
        headers = {
            'Content-Type': 'application/json',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.306 Chrome/78.0.3904.130 Electron/7.1.11 Safari/537.36',
            'Authorization': self.token
        }
        return headers

    def run(self):
        super().run(self.token, bot=False)


if __name__ == '__main__':
    client = disClient()
    run_server.keep_alive()
    client.run()
