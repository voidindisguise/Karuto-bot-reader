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
        clientsTuple(client=DiscordClient("1️⃣", 'group1', 0, 1057586818259890200), event=asyncio.Event(), token=""),
        clientsTuple(client=DiscordClient("2️⃣", 'group1', 1, 1057586818259890200), event=asyncio.Event(), token=""),
        clientsTuple(client=DiscordClient("3️⃣", 'group1', 2, 1057586818259890200), event=asyncio.Event(), token=""),
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
    