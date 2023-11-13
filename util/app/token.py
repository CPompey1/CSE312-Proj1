import secrets
import hashlib
from util.database.users import AuctionUsers

def hashAuthToken(token: str):
    tokenHash = hashlib.sha256(token.encode())
    tokenHashBytes = tokenHash.hexdigest().encode()
    return tokenHashBytes

def createAuthToken(auctionUsers: AuctionUsers,username:str):
    authToken = secrets.token_urlsafe(32)
    authTokenHash = hashAuthToken(authToken)
    auctionUsers.updateUserToken(username,authTokenHash)
    return authToken

def getUserByAuthToken(auctionUsers: AuctionUsers,token: str):
    tokenHash = hashAuthToken(token)
    return auctionUsers.findUserByToken(tokenHash)
