import os
import secrets

from pymongo import MongoClient

CLIENT = 'mongo'
DATABASE = 'auctionDb'


class AuctionDb:
    def __init__(self, collectionName):
        self.client = MongoClient("mongodb://localhost:27017")
        self.db = self.client[DATABASE]
        self.collection = self.db[collectionName]

    def insert_record(self, record):
        try:
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

    def add_item_image(self, auction_token, image_bytes):
        image_name = auction_token + ".jpg"
        # image_name = self.generate_auction_id() + ".jpg"
        file_path = "public/image/auction_images" + image_name
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'wb') as file:
            file.write(image_bytes)

        self.collection.update_one({'auction_token': auction_token}, {'$set': {'image_name': image_name}})
        return

    def get_all_auctions(self):
        return self.posts.find({})

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


