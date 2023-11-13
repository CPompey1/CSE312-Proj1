from pydoc import html

import bcrypt

from util.authToken import createAuthToken
from util.database.db import Account, Token
from util.globals import HTML_DIRECTORY
from util.response import htmlResponse


def login(account: Account, token: Token, username: str, password: str):
    userDocument = account.getAccount(html.escape(username))

    if userDocument is None:
        return htmlResponse(HTML_DIRECTORY, 'account_not_found.html', 200)

    check_password = bcrypt.checkpw(password.encode(), userDocument['password'])
    # print("checking password")
    if check_password:
        resp = htmlResponse(HTML_DIRECTORY, 'login.html', 200)
        resp.set_cookie('auth_token', createAuthToken(token, username), httponly=True, max_age=3600)
        return resp
    else:
        return htmlResponse(HTML_DIRECTORY, 'wrong_password.html', 200)