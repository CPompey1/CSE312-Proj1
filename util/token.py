import secrets
import hashlib
from util.globals import USERS, HTML_DIRECTORY

def hashAuthToken(token: str):
    tokenHash = hashlib.sha256(token.encode())
    tokenHashBytes = tokenHash.hexdigest().encode()
    return tokenHashBytes

def createAuthToken(username:str):
    authToken = secrets.token_urlsafe(32)
    authTokenHash = hashAuthToken(authToken)
    USERS.updateUserToken(username,authTokenHash)
    return authToken

def getUserByAuthToken(token: str):
    tokenHash = hashAuthToken(token)
    return USERS.findUserByToken(tokenHash)
