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
            'auctionPosts': [],
            'bids': {},
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

    def postUsersBid(self, username, auction_id: int, bid: float):
        user = self.collection.find_one_record({'_id': username})
        bids = user.get("bids", {})
        bids[auction_id] = bid
        self.collection.update_one_record(self.collection,{'_id': username},{'bids': bids})
        return
        # auctionBids = self.getAuctionByValue("_id", auctionId)
        # if (auctionBids is not None):
        #     bids = auctionBids["bids"]
        #     bids[username] = userBid