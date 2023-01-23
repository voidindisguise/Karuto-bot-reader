import pymongo
import certifi

class DataStorage:
    
    client = pymongo.MongoClient("mongodb+srv://Shrikar:Shrikar123@dashboard.ars8h.mongodb.net/?retryWrites=true&w=majority", connect=False, tlsCAFile=certifi.where())
        
    def __init__(self, dbName, collectionName):
        self.db = DataStorage.client[dbName]
        self.collection = self.db[collectionName]
    