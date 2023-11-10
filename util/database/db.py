from pymongo import MongoClient

# CLIENT = 'mongo'
CLIENT = 'localhost'
DATABASE = 'auctionDb'

class AuctionDb:
    def __init__(self,collectionName):
        self.client = MongoClient(CLIENT)
        self.db = self.client[DATABASE]
        self.collection = self.db[collectionName]
        self.counter_id = collectionName+"CounterId"
        self.counter = self.db[collectionName+"Counter"]

    def get_count(self):
        counter = self.counter.find_one_and_update({'_id': self.counter_id},{'$inc': {'count': 1}},upsert=True,return_document=True)
        return counter['count']
    
    def insert_record(self,record):
        try:
            print(record)
            self.collection.insert_one(record)
        except:
            print("error inserting record")
            return
        return 

    def find_one_record(self,record):
        return self.collection.find_one(record)
    
    def find_all_records(self,record):
        records = []
        cursor = self.collection.find(record)
        for i in cursor:
            records.append(i)
        return records
    
    def update_record(self, record_to_update, new_value):
        try:
            self.collection.find_one_and_update(record_to_update, {'$set': new_value})
        except:
            print("error updating record")
            return
    
    def delete_record(self, record_to_delete):
        try:
            self.collection.delete_one(record_to_delete)
        except:
            print("error deleting record")
            return
