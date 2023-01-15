import asyncio
import discord
from collections import namedtuple
from bot import DiscordClient
import datastoreutils

async def ClientLogin(clients):
    for _client in clients:
        await _client.client.login(_client.token, bot=False)
     
async def WrappedConnect(_client):
    try:
        await _client.client.close()
        await _client.client.clear()
    except:
        pass
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

    clients = [
        clientsTuple(client=DiscordClient("1️⃣", 'group1', 0, 1057586818259890200), event=asyncio.Event(), token="Mjk0Nzg2NTQ2MTgyMzg5NzYw.Gab33r.sLYu351EaLTrR1gklVmRG7zJsd_3n9KFw2OBG4"),
        clientsTuple(client=DiscordClient("2️⃣", 'group1', 1, 1057586818259890200), event=asyncio.Event(), token="MzAxODU2MTU0MzMyNjkyNDgw.G-QYIv.iNk3cieAhzoMpEcFl84f6cKSbU_ML9Rh5Qcey8"),
        clientsTuple(client=DiscordClient("3️⃣", 'group1', 2, 1057586818259890200), event=asyncio.Event(), token="MzE4NTAyNzA4ODk2MjAyNzUy.GFc7a5.QDATkX5OMYqQgS_k9oOW11vaIPqCaOxjbL9UHw"),
    ]
    
    pickupDropTimes = datastoreutils.GetData(['group1'])
    
    DiscordClient.lastDropTime = pickupDropTimes['lastDropTime']
    DiscordClient.lastPickupTime = pickupDropTimes['lastPickupTime']

    loop = asyncio.get_event_loop()
    loop.run_until_complete(ClientLogin(clients))
    
    for client in clients:
        loop.create_task(WrappedConnect(client))
        
    loop.run_until_complete(check_close(clients))
    
    loop.close()
    
    loop.run_forever()
    
    
    
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