import secrets
from util.database.db import Token
import hashlib
from util.globals import*

def hashAuthToken(token: str):
    tokenHash = hashlib.sha256(token.encode())
    tokenHashBytes = tokenHash.hexdigest().encode()
    return tokenHashBytes

def createAuthToken(token:Token, username:str):
    authToken = secrets.token_urlsafe(32)
    authTokenHash = hashAuthToken(authToken)
    token.createToken(username,authTokenHash)
    return authToken,authTokenHash

def getTokenUsername(token:Token, tokenInput:str):
    if(tokenInput is None):
        return None

    authTokenHash = hashAuthToken(tokenInput)
    result = token.getToken(authTokenHash)
    if result is None:
        return None
    else:
        return result['_id']
    
