from pymongo import MongoClient

class Client:
    def __init__(self):
        self.client = MongoClient("localhost")
        self.db = self.client["project2"]
    
    def createCollection(self,collectionName:str):
        return self.db[collectionName]
    
    def findDocument(self,collection, key:str, value):
        return collection.find_one({key: value})
    
    def updateDocument(self, collection, document:dict, key:str, newValue):
        try:
            collection.find_one_and_update({'_id':document['_id']},{'$set': {key: newValue}})
            return True
        except:
            return False
    
    def deleteDocument(self,collection,document:dict):
        try:
            collection.delete_one({'_id': document['_id']})
            return True
        except:
            return False

class Account(Client):
    def __init__(self, collectionName: str):
        super().__init__()
        self.accounts = self.createCollection(collectionName)

    def createAccount(self,username:str , passwordHash: bytes):
        try:
            self.accounts.insert_one({"_id": username, "password": passwordHash})
            return True
        except:
            return False
    
    def getAccount(self,username:str):
        return super().findDocument(self.accounts,'_id',username)
    
    def updateUsername(self,username:str, newUsername):
        document = self.getAccount(username)
        return super().updateDocument(self.accounts,document,"password",newUsername)
    
    def deleteAccount(self, username: str):
        document = self.getAccount(username)
        return super().deleteDocument(self.accounts,document)
    
class Token(Client):
    def __init__(self, collectionName: str):
        super().__init__()
        self.tokens = self.createCollection(collectionName)
    
    def createToken(self, username: str, token: bytes):
        try:
            self.tokens.find_one_and_update({"_id": username}, {'$set': {"tokenHash": token}},upsert=True)
            return True
        except:
            return False

    def getToken(self, tokenHash: bytes):
        return super().findDocument(self.tokens,"tokenHash",tokenHash)
    
    def updateToken(self, oldTokenHash: bytes, newTokenHash: bytes):
            document = self.getToken(oldTokenHash)
            return super().updateDocument(self.tokens,document,"tokenHash",newTokenHash)

    def deleteToken(self, token: bytes):
            document = self.getToken(token)
            return super().deleteDocument(self.tokens,document)
    
class Posts(Client):
    def __init__(self, collectionName: str):
        super().__init__()
        self.posts = self.createCollection(collectionName)
        self.postsCounter = self.createCollection(collectionName+"Conter")

    def __get_count(self):
        counter = self.postsCounter.find_one_and_update({'_id': self.counter_id},{'$inc': {'count': 1}},upsert=True,return_document=True)
        return counter['count']
    
    def createPosts(self, username: str, title: str, description: str):
        try:
            self.posts.insert_one({
                                    "_id": self.__get_count(),
                                    "username": username,
                                    "title": title,
                                    "description": description,
                                    "likes": 0,
                                    "isDeleted": False,
                                    })
            return True
        except Exception as e:
            return False

    def getPost(self, id: int):
        return super().findDocument(self.posts,'_id',id)
    
    def getAllPost(self):
        return self.posts.find({})
    
    def updatePost(self, id: int, key:str, newValue):
        document = self.getPost(self,id)
        if(key == "likes"):
            return super().updateDocument(self.posts,document,"likes", newValue)
        elif(key == "isDeleted"):
            return super().updateDocument(self.posts,document,"isDeleted", newValue)

    def deletePost(self, id: int):
            document = self.getPost(id)
            return super().deleteDocument(self.posts,document)
                