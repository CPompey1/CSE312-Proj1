import os
import secrets

from pymongo import MongoClient

# CLIENT = 'mongo'
CLIENT = 'localhost'
DATABASE = 'auctionDb'


class AuctionDb:
    def __init__(self, collectionName):
        self.client = MongoClient("mongo")
        self.db = self.client[DATABASE]
        self.collection = self.db[collectionName]
        self.counter_id = collectionName+"CounterId"
        self.counter = self.db[collectionName+"Counter"]

    def get_count(self):
        counter = self.counter.find_one_and_update({'_id': self.counter_id},{'$inc': {'count': 1}},upsert=True,return_document=True)
        return counter['count']
    
    def find_index(self):
        result = self.collection.find_one({'_id': 0})

        if result:
            curr_id = result.get('current_index')
            self.collection.update_one({'_id': 0}, {'$set': {'current_index': (curr_id + 1)}})
        else:
            curr_id = 1
            self.collection.insert_one({
                '_id': 0,
                'current_index': 2
            })
        return curr_id

    def insert_record(self, record):
        try:
            print(record)
            self.collection.insert_one(record)
        except:
            print("error inserting record")
            return
        return

    def find_one_record(self, record):
        return self.collection.find_one(record)

    def find_all_records(self, record):
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

    def findDocument(self, collection, key: str, value):
        return collection.find_one({key: value})



class Auction(AuctionDb):
    def __init__(self):
        super().__init__('auctions')

    def generate_auction_id(self, auction_id):
        token = secrets.token_hex(16)
        self.collection.update_one({'_id': auction_id}, {'$set': {'auction_token': token}})
        return token

    def add_item_image(self, auction_id):
        # , image_bytes
        image_name = str(auction_id) + ".jpg"
        # image_name = self.generate_auction_id() + ".jpg"
        # file_path = "public/image/auction_images" + image_name
        # os.makedirs(os.path.dirname(file_path), exist_ok=True)
        #
        # with open(file_path, 'wb') as file:
        #     file.write(image_bytes)

        self.collection.update_one({'_id': auction_id}, {'$set': {'image_name': image_name}})
        return

    def get_all_auctions(self):
        return self.collection.find({"_id": {"$ne": 0}})

    def update_highest_bid(self, auction_id, bid):
        return self.collection.update_one({"_id": auction_id}, {"$set": {"highest_bid": bid}})

    def add_new_auction(self, name, category):
        item_id = self.find_index()
        auction = {
            '_id': item_id,
            'item_name': name,
            'category': category,
        }
        self.insert_record(auction)
        return

    def get_auction_category(self, category):
        return self.collection.find({'category': category})

    def delete_all(self):
        return self.collection.delete_many({})


class Account(AuctionDb):
    def __init__(self):
        super().__init__('accounts')

    def getAccount(self,username:str):
        return super().findDocument(self.collection, '_id', username)

    def createAccount(self, username: str, passwordHash: bytes):
        try:
            self.collection.insert_one({"_id": username, "password": passwordHash})
            return True
        except:
            return False


class Token(AuctionDb):
    def __init__(self):
        super().__init__('tokens')

    def createToken(self, username: str, token: bytes):
        try:
            self.collection.find_one_and_update({"_id": username}, {'$set': {"tokenHash": token}}, upsert=True)
            return True
        except:
            return False


