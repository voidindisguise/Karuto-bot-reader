import json
import datetime

def UpdatePickupTime(botGroupName, botIdInGroup, date):
    with open("pickupdroptimes.json", "r") as f:
        data = json.load(f)
    
    data['lastPickupTime'][botGroupName][botIdInGroup] = date.strftime("%Y-%m-%d %H:%M:%S")
    
    with open("pickupdroptimes.json", "w") as f:
        json.dump(data, f)
        
def UpdateDropTime(botGroupName, botIdInGroup, date):
    with open("pickupdroptimes.json", "r") as f:
        data = json.load(f)
    
    data['lastDropTime'][botGroupName][botIdInGroup] = date.strftime("%Y-%m-%d %H:%M:%S")
    
    with open("pickupdroptimes.json", "w") as f:
        json.dump(data, f)
    
def GetLastPickupTime(botGroupName, botIdInGroup):
    with open("pickupdroptimes.json", "r") as f:
        data = json.load(f)
    return datetime.datetime.strptime(data['lastPickupTime'][botGroupName][botIdInGroup], "%Y-%m-%d %H:%M:%S")

def GetLastDropTime(botGroupName, botIdInGroup):
    with open("pickupdroptimes.json", "r") as f:
        data = json.load(f)
    return datetime.datetime.strptime(data['lastDropTime'][botGroupName][botIdInGroup], "%Y-%m-%d %H:%M:%S")

def GetLastPickupTimeGroup(botGroupName):
    with open("pickupdroptimes.json", "r") as f:
        data = json.load(f)
    return [datetime.datetime.strptime(timestring, "%Y-%m-%d %H:%M:%S") for timestring in data['lastPickupTime'][botGroupName]]

def GetLastDropTimeGroup(botGroupName):
    with open("pickupdroptimes.json", "r") as f:
        data = json.load(f)
    return [datetime.datetime.strptime(timestring, "%Y-%m-%d %H:%M:%S") for timestring in data['lastDropTime'][botGroupName]]

def GetData(groups):
    lastDropTime = {}
    lastPickupTime = {}
    for g in groups:
        lastDropTime[g] = GetLastDropTimeGroup(g)
        lastPickupTime[g] = GetLastPickupTimeGroup(g)
        
    return {
        'lastDropTime': lastDropTime,
        'lastPickupTime': lastPickupTime
    }