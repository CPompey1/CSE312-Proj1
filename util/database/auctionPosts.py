from util.database.db import AuctionDb
import datetime

AUCTIONS ='auctionPosts'


class AuctionPosts:
    def __init__(self):
        self.collection = AuctionDb(AUCTIONS)
        
    def insertAuction(self, username:str,title:str, description:str, imageUrl:str,startingPrice:float,endTime: datetime, category:str):
        
        record = {
                  "_id": self.collection.get_count(), 
                  "username":username,
                  "title": title,
                  "description":description,
                  "imageUrl":imageUrl,
                  "startingPrice":startingPrice,
                  "endTime":endTime,
                  "category":category,
                  "highestBid":startingPrice,
                  "bids": [],
                  "active": True
                  }
        
        self.collection.insert_record(record)
        return
    
    def getAuctionByValue(self, field:str, value):
        record = {field: value}
        return self.collection.find_one_record(record)
    
    def getAuctionsByCategory(self, catergory:str):
        cursor =  self.collection.find_all_records({"category": catergory})
        out = []
        for ele in cursor:
            out.append(ele)
        return out
    
    def getAuctionsByUser(self, user:str):
        return self.collection.find_all_records({"username": user})
    def endAuction(self,auctionId):
        self.collection.update_record({'_id':auctionId},{"active": False})
        return
    
    def getAllAuctionsAsList(self):
        return self.collection.find_all_records({})
        # out = []
        # for ele in cursor:
        #     out.append(ele)
        # return out
    
    def getAuctionsByCategoryAsList(self, catergory:str):
        cursor = self.collection.find_all_records({"category": catergory})
        out = []
        for ele in cursor:
            out.append(ele)
        return out
    #gets user specific auctions (seperated into won and created)
    def getUserAuctions(self,user:str):
        out = {}
        cursor = self.collection.find_all_records({"username": user,
                                                   "active":True})
        out['Created Auctions'] = []
        for ele in cursor:
            out["Created Auctions"].append(ele)
            
        out['Won Auctions'] = []
        cursor = self.collection.find_all_records({"username": user,
                                                   "active":False})
        for ele in cursor:
            out["Won Auctions"].append(ele)
        return out
    #gets all  auctions (seperated into won and created)
    def getAllAuctions(self):
        out = {}
        cursor = self.collection.find_all_records({"active":True})
        out['Created Auctions'] = []
        for ele in cursor:
            out["Created Auctions"].append(ele)
            
        out['Won Auctions'] = []
        cursor = self.collection.find_all_records({"active":False})
        for ele in cursor:
            out["Won Auctions"].append(ele)
        return out
    def updateBids(self, auctionId: int, username:str, userBid: float):
       auctionBids = self.getAuctionByValue("_id",auctionId)
       if(auctionBids is not None):
           bids = auctionBids["bids"]
           bids[username] = userBid
           self.collection.update_record({"_id": auctionId},{"bids": bids})
           return
       