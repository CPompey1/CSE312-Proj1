from util.database.db import AuctionDb
import html

USERS = 'users'

class AuctionUsers:
    def __init__(self):
        self.collection = AuctionDb(USERS)

    def insertUsers(self, username: str, passwordHash: bytes):
        record = {
            '_id': html.escape(username),
            'password': passwordHash,
            'token': b"",
            'auctionsWon': [],
            'auctionPosts': []
        }
        try:
            self.collection.insert_record(record)
            return True
        except:
            return False

    def getAuctionByValue(self, field:str, value):
        record = {field: value}
        return self.collection.find_one_record(record)
    
    def updateUsersWonAuctions(self, username:str ,auctionId: int):
       user = self.collection.find_one_record({"_id": username})
       if(username is not None):
           auctionsWon = user["auctionsWon"]
           auctionsWon.append(auctionId) 
           self.collection.update_record({"_id": username},{"auctionsWon": auctionsWon})
           return
    
    def updateUsersAuctionPosts(self, username:str ,auctionId: int):
       user = self.collection.find_one_record({"_id": username})
       if(username is not None):
           auctionPosts = user["auctionPosts"]
           auctionPosts.append(auctionId) 
           self.collection.update_record({"_id": username},{"auctionPosts": auctionPosts})
           return

    def updateUserToken(self, username:str, newToken:bytes):
        self.collection.update_record({"_id":username}, {"token" : newToken})
        return
    
    def findUserByToken(self, tokenHash:bytes):
        return self.collection.find_one_record({"token": tokenHash})