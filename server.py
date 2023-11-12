from markupsafe import escape
import os,sys
from flask import Flask,request,make_response, render_template,send_from_directory, send_from_directory, jsonify
# from sock import Sock

from flask_sock import Sock
from util.database.auctionPosts import AuctionPosts
from time import sleep
from util.globals import  AUCTION, USERS
from datetime import datetime

app = Flask(__name__)
socket = Sock(app)
example = datetime(2023,1,1,12,1,2)


def start_list():
    AUCTION.insertAuction("anthony","car","car description", "image.jpg", 4.11, example,"cars")

@app.route("/")
def index():
    resp = make_response(send_from_directory('public/html', 'index.html'))
    # add headers
    resp.headers['X-Content-Type-Options'] = 'nosniff'

    return resp

# @app.route("/create_auction")
# def create_auction_handler():
#     resp = make_response(send_from_directory('public/html', 'create_auction.html'))
#     # add headers
#     resp.headers['X-Content-Type-Options'] = 'nosniff'

#     return resp

# @app.route("/auctions_won")
# def auction_won_handler():
#     resp = make_response(send_from_directory('public/html', 'auctions_won.html'))
#     # add headers
#     resp.headers['X-Content-Type-Options'] = 'nosniff'

#     return resp

# @app.route("/closed_auctions")
# def closed_auctions_handler():
#     resp = make_response(send_from_directory('public/html', 'closed_auctions.html'))
#     # add headers
#     resp.headers['X-Content-Type-Options'] = 'nosniff'

#     return resp



@app.route("/post-history")
def allHistory():
    auctions = AUCTION.getAllAuctionsAsList()
    postHistory = []
    for auction in auctions:
        postHistory.append({
            "auctionId":auction["_id"],
            "itemName":auction["title"],
            "description": auction["description"],
            "highestBid": max(auction["bids"].items(), key = lambda x: x[1]),
            "imageUrl": auction["imageUrl"]
        })

    print(postHistory,file=sys.stderr)
    resp = make_response(jsonify(postHistory))
    resp.mimetype = 'application/json'
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    return resp

# @app.route("/post-history/<category>")
# def historyHandler(category):
#     # AUCTION.delete_all()
#     print(category)
#     auctions = AUCTION.get_auction_category(category)
#     auctionHistory = []
#     # auth_token = request.cookies.get('auth_token')
#     for item in auctions:
#         print(item)
#         auctionHistory.append({'_id': item['_id'],
#                                'item_name': item['item_name'],
#                                'category': item['category'],
#                                'highest_bid': item['highest_bid'],
#                                'image_name': item['image_name']
#                                })
#     resp = make_response(jsonify(auctionHistory))
#     resp.mimetype = 'application/json'
#     resp.headers['X-Content-Type-Options'] = 'nosniff'
#     return resp

# @app.route("/register", methods=['POST'])
# def handleRegister():
#     # print(request.form, file=sys.stderr)
#     username = request.form.get('username_reg')
#     password = request.form.get('password_reg')
#     return register(ACCOUNT, username, password)


# @app.route("/login", methods=['POST'])
# def handleLogin():
#     print("handle login")
#     username = request.form.get('username_login')
#     password = request.form.get('password_login')
#     return login(ACCOUNT, TOKEN, username, password)

@app.route("/<path:path>")
def getPage(path):
    # print(path)
    root = '.'
    if not path.__contains__("public"):
        root = 'public'
    resp = make_response(send_from_directory(root,path))
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    return resp

# @socket.route('/getAllAuctions')
# def getAllAuctions(sock):
#     auctions = AuctionPosts()
#     startSig =  sock.receive()
#     while True:
#         sleep(1)
#         data = auctions.getAllAuctionsAsList()
#         sock.send(data)
    
# @socket.route('/getAllAuctions/<path:path>')
# def getAllAuctionsCat(sock, path):
#     auctions = AuctionPosts()
#     startSig =  sock.receive()
#     while True:
#         sleep(1)
#         data = auctions.getAuctionsByCategoryAsList(path)
#         sock.send(data)
    

if __name__ == "__main__":
    #start_list()
    #AUCTION.updateBids(1,"anthony",5.11)
    app.run('0.0.0.0',8080)
    
