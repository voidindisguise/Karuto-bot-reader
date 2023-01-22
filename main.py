import asyncio
from collections import namedtuple
from bot import DiscordClient
import datetime
from utils import GetValidTokens

async def ClientLogin(clients):
    for _client in clients:
        await _client.client.login(_client.token, bot=False)
     
async def WrappedConnect(_client):
    try:
        await _client.client.connect()
    except Exception as e:
        await _client.client.close()
        print('We got an exception: ', e.__class__.__name__, e)
        _client.event.set()
        
async def check_close(clients):
    futures = [_client.event.wait() for _client in clients]
    await asyncio.wait(futures)
        

if __name__ == '__main__':
    clientsTuple = namedtuple('ClientsTuple', ['client', 'event', 'token'])
    validGroups = {}
    
    GetValidTokens(validGroups)
    
    clients = []
    
    for groupName in validGroups:
        if len(validGroups[groupName]['tokens']) > 0:
            DiscordClient.lastDropTime[groupName] = []
            DiscordClient.lastPickupTime[groupName] = []
            DiscordClient.turnToDrop[groupName] = []
            DiscordClient.canPickup[groupName] = []
            DiscordClient.canDrop[groupName] = []
            DiscordClient.batches[groupName] = []
        reactions = ["1️⃣", "2️⃣", "3️⃣"]
        reactionToBeAdded = 0
        for ind in range(len(validGroups[groupName]['tokens'])):
            if ind%3 == 0:                
                DiscordClient.lastDropTime[groupName].append([])
                DiscordClient.lastPickupTime[groupName].append([])
                DiscordClient.turnToDrop[groupName].append(0)
                DiscordClient.canPickup[groupName].append([])
                DiscordClient.canDrop[groupName].append([])
                DiscordClient.batches[groupName].append([])
            
            DiscordClient.lastDropTime[groupName][-1].append(datetime.datetime.utcnow())
            DiscordClient.lastPickupTime[groupName][-1].append(datetime.datetime.utcnow())
            DiscordClient.canPickup[groupName][-1].append(False)
            DiscordClient.canDrop[groupName][-1].append(False)
            DiscordClient.batches[groupName][-1].append(0)
            
            clients.append(clientsTuple(
                client = DiscordClient(
                    reactions[reactionToBeAdded],
                    groupName,
                    ind//3,
                    reactionToBeAdded,
                    validGroups[groupName]['channelId']
                ),
                event = asyncio.Event(),
                token = validGroups[groupName]['tokens'][ind]
            ))
            reactionToBeAdded = (reactionToBeAdded + 1)%3 
    
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ClientLogin(clients))
    
    for client in clients:
        loop.create_task(WrappedConnect(client))
        
    loop.run_until_complete(check_close(clients))
    
    loop.close()
    
    
    # tokens = [
    #     "MzAxODU2MTU0MzMyNjkyNDgw.G-QYIv.iNk3cieAhzoMpEcFl84f6cKSbU_ML9Rh5Qcey8",
    #     "MzQ5NzQ4NDcxMjgyMDA4MDc0.GP2Fc4.2JL9ebzZHX0oCBp5cOlsEKNz_eMzOlLTsml33s",
    #     "MzQ3NDEyNjc2OTgyNDcyNzA1.GeV7iP.ccmR40sn9Kq_L0r4gif-NRSG3C6t6rqxDzPq1g",
    #     "MzkyOTEyNjQ4NzE2NjgxMjE4.G23c7y.7Lavtb2_XeDiW6BaBAiCRcMNWSfpHxSrEcBuUc",
    #     "MzE4NTAyNzA4ODk2MjAyNzUy.GFc7a5.QDATkX5OMYqQgS_k9oOW11vaIPqCaOxjbL9UHw",
    #     "Mjk0Nzg2NTQ2MTgyMzg5NzYw.Gab33r.sLYu351EaLTrR1gklVmRG7zJsd_3n9KFw2OBG4",
    #     "MzExNTgwMDY1ODExMDA1NDQw.Gnl7qG.jCbWWeGiJzq16yZqegWMDLTo32N4rL4FJ-nUZY",
    #     "MzU1MzM0ODMxODIwODk4MzI1.GA4xNu.7Wlb450Fpht4TT3g-LWLTioOCEWV0-OWZdH63U",
    #     "MzU1MjcwNDk2NTExODUyNTc2.GvJh_v.P9UxlbwAIu19g0HnyL10hG8AjE4J3aJKXS24MY"
    # ]
    
    # {"type":3,"nonce":"1064180542750064640","guild_id":"1057586818259890197","channel_id":"1057586818259890200","message_flags":0,"message_id":"1064180141833596958","application_id":"646937666251915264","session_id":"412019381c9321e943f7677af6b3966e","data":{"component_type":2,"custom_id":"e35b25af-9e0f-4e1d-9b83-5bf48f2188db"}}
    # {"type":3,"nonce":"1064180780705513472","guild_id":"1057586818259890197","channel_id":"1057586818259890200","message_flags":0,"message_id":"1064180395412832307","application_id":"646937666251915264","session_id":"412019381c9321e943f7677af6b3966e","data":{"component_type":2,"custom_id":"5c88206d-f980-406e-ae87-ad477c78c03a"}}
    
    
    