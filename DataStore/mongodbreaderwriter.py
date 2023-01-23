import DataStore.mongodbconnector as mongodbconnector
import datetime


def UpdatePickupTime(botId, date):
    ds = mongodbconnector.DataStorage('KarutaReader', "pickupdroptimes")
    ds.collection.update_one({
        "botId": botId
    }, {
        "$set": {
            'lastPickupTime': date.strftime("%Y-%m-%d %H:%M:%S")
        }
    })


def UpdateDropTime(botId, date):
    ds = mongodbconnector.DataStorage('KarutaReader', "pickupdroptimes")
    ds.collection.update_one({
        "botId": botId
    }, {
        "$set": {
            'lastDropTime': date.strftime("%Y-%m-%d %H:%M:%S")
        }
    })


def GetLastPickupTime(botId):
    ds = mongodbconnector.DataStorage('KarutaReader', "pickupdroptimes")
    result = ds.collection.find_one({
        "botId": botId
    })
    return result['lastPickupTime']


def GetLastDropTime(botId):
    ds = mongodbconnector.DataStorage('KarutaReader', "pickupdroptimes")
    result = ds.collection.find_one({
        "botId": botId
    })
    return datetime.datetime.strptime(result['lastDropTime'], "%Y-%m-%d %H:%M:%S")

def GetData():
    data = {}
    ds = mongodbconnector.DataStorage('KarutaReader', "pickupdroptimes")
    cursor = ds.collection.find_all({
        
    })
    for row in cursor:
        data[row['botId']] = {}
        data[row['botId']]['lastPickupTime'] = datetime.datetime.strptime(row['lastPickupTime'], "%Y-%m-%d %H:%M:%S")
        data[row['botId']]['lastDropTime'] = datetime.datetime.strptime(row['lastDropTime'], "%Y-%m-%d %H:%M:%S")

    return data

def insertDataIfNotPresent(botId):
    ds = mongodbconnector.DataStorage('KarutaReader', 'pickupdroptimes')
    data = ds.collection.find_one({"botId": botId})
    if not data:
        data = {
            "botId": botId,
            "lastPickupTime": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            'lastDropTime': datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        }
        ds.collection.insert_one(data)
    return data