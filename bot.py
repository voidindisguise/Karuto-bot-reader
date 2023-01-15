import requests
from discord.ext import commands
import datetime
import asyncio
import datastoreutils

class DiscordClient(commands.Bot):
    
    lastDropTime = {
        "group1": [
            datetime.datetime.utcnow(),
            datetime.datetime.utcnow(),
            datetime.datetime.utcnow()
        ]
    }
    
    turnToDrop = {
        "group1": 0
    }
    
    canDrop = {
        "group1": [False, False, False]
    }
    
    canPickup = {
        "group1": [False, False, False]
    }
    
    lastPickupTime = {
        "group1": [
            datetime.datetime.utcnow(),
            datetime.datetime.utcnow(),
            datetime.datetime.utcnow()
        ]
    }
    
    def __init__(self, reactionToBeAdded, botGroupName, botIdInGroup, channelIdActiveIn):
        super().__init__(command_prefix=':')
        self.session = requests.Session()
        self.remove_command('help')
        self.reactionToBeAdded = reactionToBeAdded
        self.botGroupName = botGroupName
        self.botIdInGroup = botIdInGroup
        self.channelIdActiveIn = channelIdActiveIn
        
    @staticmethod
    def UpdateLastDropTime(groupName, botIdInGroup):
        DiscordClient.lastDropTime[groupName][botIdInGroup] = datetime.datetime.utcnow()
        datastoreutils.UpdateDropTime(groupName, botIdInGroup, DiscordClient.lastDropTime[groupName][botIdInGroup])
    
    @staticmethod
    def UpdateLastPickupTime(groupName, botIdInGroup):
        DiscordClient.lastPickupTime[groupName][botIdInGroup] = datetime.datetime.utcnow()
        datastoreutils.UpdatePickupTime(groupName, botIdInGroup, DiscordClient.lastPickupTime[groupName][botIdInGroup])
    
    @staticmethod
    def UpdateCanPickup(groupName, botIdInGroup):
        DiscordClient.canPickup[groupName][botIdInGroup] = (int((datetime.datetime.utcnow() - DiscordClient.lastPickupTime[groupName][botIdInGroup]).total_seconds()//60) >= 12)
            
    @staticmethod
    def UpdateCanDrop(groupName, botIdInGroup):
        DiscordClient.canDrop[groupName][botIdInGroup] = (int((datetime.datetime.utcnow() - DiscordClient.lastDropTime[groupName][botIdInGroup]).total_seconds()//60) >= 32)
        
    @staticmethod
    def UpdateTurnToDrop(groupName, botIdInGroup):
        DiscordClient.turnToDrop[groupName] = botIdInGroup
        
    @staticmethod
    def CanGroupPickup(groupName):
        return (DiscordClient.canPickup[groupName][0] and DiscordClient.canPickup[groupName][1]) and DiscordClient.canPickup[groupName][2]
       
    @staticmethod
    def CanGroupDrop(groupName):
        return (DiscordClient.canDrop[groupName][0] and DiscordClient.canDrop[groupName][1]) and DiscordClient.canDrop[groupName][2]
        
    @staticmethod
    def IsTurnToDrop(groupName, botIdInGroup):
        return DiscordClient.turnToDrop[groupName] == botIdInGroup
        
    async def on_ready(self):
        print(f"User online : {self.user.id}")
        await self.get_channel(self.channelIdActiveIn).send("Hello guys, let's start playing!")
        
            
    async def on_message(self, message):
        if message.author.id == self.user.id and message.content == "Hello guys, let's start playing!":
            print(self.user.id, "\n")
        
            #Card Drop Code
            while 1:        
                if (DiscordClient.CanGroupDrop(self.botGroupName) and DiscordClient.IsTurnToDrop(self.botGroupName, self.botIdInGroup)) and DiscordClient.CanGroupPickup(self.botGroupName):
                    channel = self.get_channel(self.channelIdActiveIn)
                    await channel.send("kd")
                    DiscordClient.UpdateLastDropTime(self.botGroupName, self.botIdInGroup)
                    DiscordClient.UpdateTurnToDrop(self.botGroupName, (self.botIdInGroup + 1)%3)
                DiscordClient.UpdateCanDrop(self.botGroupName, self.botIdInGroup)
                DiscordClient.UpdateCanPickup(self.botGroupName, self.botIdInGroup)    
                await asyncio.sleep(10)
        

    async def on_reaction_add(self, reaction, user):
        if (reaction == self.reactionToBeAdded and user.id == 646937666251915264) and (reaction.channel.id == self.channelIdActiveIn and DiscordClient.canPickup[self.botGroupName][self.botIdInGroup]):
            print(reaction)
            await asyncio.sleep(1)
            await reaction.message.add_reaction(self.reactionToBeAdded)
            DiscordClient.UpdateLastPickupTime(self.botGroupName, self.botIdInGroup)
            DiscordClient.UpdateCanPickup(self.botGroupName, self.botIdInGroup)