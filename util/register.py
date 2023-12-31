import bcrypt
from util.database.db import Account
from util.database.users import AuctionUsers
from flask import make_response
from util.response import htmlResponse
import html
from util.globals import *

def register(account: Account ,username:str, password:str):    
    if account.getAccount(username) is not None:
        return htmlResponse(HTML_DIRECTORY,'account_already_exists.html',200)

    usernameHtmlEscaped = html.escape(username)
    passwordHash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    createAccountResult = account.createAccount(usernameHtmlEscaped,passwordHash)
    USERS.insertUsers(usernameHtmlEscaped,passwordHash=passwordHash,tokenHash=None)
    if createAccountResult: 
        return htmlResponse(HTML_DIRECTORY,'register.html',200)
    else:
        return make_response("error", 200)
    