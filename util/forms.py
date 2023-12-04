from util.globals import HTML_DIRECTORY
import bcrypt
from util.response import htmlResponse
from util.token import createAuthToken, hashAuthToken
from util.database.users import AuctionUsers

USERS2 = AuctionUsers()

def auction_register(username:str, password:str, email:str):
    if USERS2.insertUsers(username,bcrypt.hashpw(password.encode(),bcrypt.gensalt()), email) == True:
        return htmlResponse(HTML_DIRECTORY,'register.html',200)
    else:
        return htmlResponse(HTML_DIRECTORY, 'account_already_exists.html', 200)

def auction_login(username:str, password:str):
    user = USERS2.getAuctionByValue('_id',username)
    if user is None:
        return htmlResponse(HTML_DIRECTORY,'account_not_found.html',200)
    
    check = bcrypt.checkpw(password.encode(),user['password'])

    if check == True:
        authToken = createAuthToken(username,)
        response = htmlResponse(HTML_DIRECTORY, 'login.html', 200)
        response.set_cookie("auth_token",authToken,3600,path='/',httponly=True)
        return response
    else:
        return htmlResponse(HTML_DIRECTORY,'wrong_password.html',200)


def getUsername(auth_token:str):
    user = USERS2.findUserByToken(hashAuthToken(auth_token))
    return user['_id']

