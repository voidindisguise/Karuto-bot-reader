import discord
import json
import asyncio 
from discord.ext import commands

class SimpleLogin(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=':')
        self.remove_command('help')
        

def GetValidTokens(validGroups):
    with open('tokens.json', 'r') as f:
        tokens = json.load(f)
    for group in tokens:
        validGroups[group['id']] = {
            "tokens": [],
            "channelId": group['channelId']
        }
        for token in group['tokens']:
            loop = asyncio.get_event_loop()
            isValid = loop.run_until_complete(IsValidToken(token))
            if isValid:
                validGroups[group['id']]['tokens'].append(token)
              
async def IsValidToken(token):
    try:
        client = discord.Client()
        await client.login(token, bot=False)
        await client.close()
        return True
    except:
        return False
    