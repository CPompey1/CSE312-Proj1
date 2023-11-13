from util.database.db import Account, Token, Auction
from util.database.users import AuctionUsers

#Mongo DB Collections
AUCTION = Auction()
ACCOUNT = Account()
USERS = AuctionUsers()
TOKEN = Token()

#Directory Paths
HTML_DIRECTORY = "public/html"
