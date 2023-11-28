from util.database.db import Account, Token, Auction
from util.database.users import AuctionUsers
from util.database.auctionPosts import AuctionPosts

#Mongo DB Collections
AUCTIONPOSTS = AuctionPosts()
AUCTION = Auction()
ACCOUNT = Account()
USERS = AuctionUsers()
TOKEN = Token()

#Directory Paths
HTML_DIRECTORY = "public/html"
