
import re
import os
import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='c!', intents=intents)

@bot.event
async def on_ready():
    print("Bot is ready")
    await bot.change_presence(activity=discord.Game(name="Fusion is Gay"), status=discord.Status.dnd)

@bot.event
async def on_message(message):
    if (bot.user != message.author):
        match = re.findall(r'(?:\✨|💰)\s([\d,]+)\s·\s([\w\s]+)\s·\s([\w\s\(★]+)', message.content)
        resources = []
        for m in match:
           resources.append(f"{m[1]} {int(m[0].replace(',',''))}")
        final_msg = ", ".join(resources)
        if final_msg:   
            await message.channel.send(final_msg)
    

bot.run(os.env.get("BOT_TOKEN"))
