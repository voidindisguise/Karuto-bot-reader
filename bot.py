import requests
from discord.ext import commands
import datetime
import asyncio
import datastoreutils
import random
import DataStore.mongodbreaderwriter as mongodbreaderwriter

class DiscordClient(commands.Bot):
    
    lastDropTime = {}
    lastPickupTime = {}
    turnToDrop = {}
    canPickup = {}
    canDrop = {}
    batches = {}
    
    def __init__(self, reactionToBeAdded, botGroupName, botBatchIdInGroup, botIdInBatch, channelIdActiveIn):
        super().__init__(command_prefix=':')
        self.session = requests.Session()
        self.remove_command('help')
        self.reactionToBeAdded = reactionToBeAdded
        self.botGroupName = botGroupName
        self.botBatchIdInGroup = botBatchIdInGroup
        self.botIdInBatch = botIdInBatch
        self.channelIdActiveIn = channelIdActiveIn
        
    @staticmethod
    def UpdateLastDropTime(groupName, botBatchIdInGroup, botIdInBatch):
        DiscordClient.lastDropTime[groupName][botBatchIdInGroup][botIdInBatch] = datetime.datetime.utcnow()
        
    
    @staticmethod
    def UpdateLastPickupTime(groupName, botBatchIdInGroup, botIdInBatch):
        DiscordClient.lastPickupTime[groupName][botBatchIdInGroup][botIdInBatch] = datetime.datetime.utcnow()
        
    
    @staticmethod
    def UpdateCanPickup(groupName, botBatchIdInGroup, botIdInBatch):
        DiscordClient.canPickup[groupName][botBatchIdInGroup][botIdInBatch] = (int((datetime.datetime.utcnow() - DiscordClient.lastPickupTime[groupName][botBatchIdInGroup][botIdInBatch]).total_seconds()//60) >= 11)
            
    @staticmethod
    def UpdateCanDrop(groupName, botBatchIdInGroup, botIdInBatch):
        DiscordClient.canDrop[groupName][botBatchIdInGroup] = (int((datetime.datetime.utcnow() - DiscordClient.lastDropTime[groupName][botBatchIdInGroup][botIdInBatch]).total_seconds()//60) >= 32)
        if DiscordClient.canDrop[groupName][botBatchIdInGroup]:
            DiscordClient.UpdateTurnToDrop(groupName, botBatchIdInGroup)
            
    @staticmethod
    def UpdateTurnToDrop(groupName, botBatchIdInGroup):
        min_time = DiscordClient.lastDropTime[groupName][botBatchIdInGroup][0]
        for t in range(len(DiscordClient.canDrop[groupName][botBatchIdInGroup])):
            if DiscordClient.canDrop[groupName][botBatchIdInGroup][t]:
                if min_time > DiscordClient.lastDropTime[groupName][botBatchIdInGroup][t]:
                    DiscordClient.turnToDrop[groupName] = t
                    min_time = DiscordClient.lastDropTime[groupName][botBatchIdInGroup][t]
                            
    @staticmethod
    def CanGroupPickup(groupName, botBatchIdInGroup):
        out = True
        for t in range(len(DiscordClient.canPickup[groupName][botBatchIdInGroup])):
            out = out and DiscordClient.canPickup[groupName][botBatchIdInGroup][t]
        return out
    
    @staticmethod
    def CanDrop(groupName, botBatchIdInGroup):
        return DiscordClient.canDrop[groupName][botBatchIdInGroup]
        
    @staticmethod
    def IsTurnToDrop(groupName, botBatchIdInGroup, botIdInBatch):
        return DiscordClient.turnToDrop[groupName][botBatchIdInGroup] == botIdInBatch
        
    async def on_ready(self):
        print(f"User online : {self.user.id}")
        data = mongodbreaderwriter.insertDataIfNotPresent(self.user.id)
        DiscordClient.lastDropTime[self.botGroupName][self.botBatchIdInGroup][self.botIdInBatch] = datetime.datetime.strptime(data['lastDropTime'], "%Y-%m-%d %H:%M:%S")
        DiscordClient.lastPickupTime[self.botGroupName][self.botBatchIdInGroup][self.botIdInBatch] = datetime.datetime.strptime(data['lastPickupTime'], "%Y-%m-%d %H:%M:%S")
        DiscordClient.batches[self.botGroupName][self.botBatchIdInGroup][self.botIdInBatch] = self.user.id
        
        await asyncio.sleep(10)
        #Card Drop Code
        while 1:   
            if (DiscordClient.CanDrop(self.botGroupName, self.botBatchIdInGroup) and DiscordClient.IsTurnToDrop(self.botGroupName, self.botBatchIdInGroup, self.botIdInBatch)) and DiscordClient.CanGroupPickup(self.botGroupName, self.botBatchIdInGroup):
                channel = self.get_channel(self.channelIdActiveIn)
                await channel.send("kd")
                DiscordClient.UpdateLastDropTime(self.botGroupName, self.botBatchIdInGroup, self.botIdInBatch)
                DiscordClient.UpdateCanDrop(self.botGroupName, self.botBatchIdInGroup, self.botIdInBatch)
                DiscordClient.UpdateCanPickup(self.botGroupName, self.botBatchIdInGroup, self.botIdInBatch)    
                DiscordClient.UpdateTurnToDrop(self.botGroupName, self.botBatchIdInGroup)
            else:
                DiscordClient.UpdateCanDrop(self.botGroupName, self.botBatchIdInGroup, self.botIdInBatch)
                DiscordClient.UpdateCanPickup(self.botGroupName, self.botBatchIdInGroup, self.botIdInBatch)    
            await asyncio.sleep(10)
        
        

    async def on_reaction_add(self, reaction, user):
        if (reaction.emoji == self.reactionToBeAdded and user.id == 646937666251915264) and (reaction.message.channel.id == self.channelIdActiveIn and DiscordClient.canPickup[self.botGroupName][self.botBatchIdInGroup][self.botIdInBatch]):
            for user in reaction.message.mentions:
                if user.id in DiscordClient.batches[self.botGroupName][self.botBatchIdInGroup][self.botIdInBatch]:        
                    await asyncio.sleep(random.random()+random.randint(1,3))
                    await reaction.message.add_reaction(self.reactionToBeAdded)
                    DiscordClient.UpdateLastPickupTime(self.botGroupName, self.botBatchIdInGroup, self.botIdInBatch)
                    DiscordClient.UpdateCanPickup(self.botGroupName, self.botBatchIdInGroup, self.botIdInBatch)