import secrets
import hashlib
from util.globals import USERS, HTML_DIRECTORY
from util.database.users import AuctionUsers

def hashAuthToken(token: str):
    tokenHash = hashlib.sha256(token.encode())
    tokenHashBytes = tokenHash.hexdigest().encode()
    return tokenHashBytes

def createAuthToken(username:str):
    authToken = secrets.token_urlsafe(32)
    authTokenHash = hashAuthToken(authToken)
    AuctionUsers().updateUserToken(username,authTokenHash)
    return authToken

def getUserByAuthToken(token: str):
    tokenHash = hashAuthToken(token)
    return AuctionUsers().findUserByToken(tokenHash)
