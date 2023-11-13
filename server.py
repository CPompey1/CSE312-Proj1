from markupsafe import escape
import os,sys
from flask import Flask,request,make_response, render_template,send_from_directory, send_from_directory, jsonify
from flask_sock import Sock
from util.database.auctionPosts import AuctionPosts
from time import sleep
from util.globals import ACCOUNT, TOKEN, AUCTION
from util.login import login
from util.register import register
from util.authToken import *
from util.database.users import AuctionUsers
from werkzeug.utils import secure_filename
from threading import *
app = Flask(__name__)
socket = Sock(app)
sockets = []
@app.route("/")
def index():
    # AUCTION.add_new_auction("bentley","cars")
    # AUCTION.update_highest_bid(1, "100")
    # AUCTION.add_item_image(1)
    #
    # AUCTION.add_new_auction("skirt","clothes")
    # AUCTION.update_highest_bid(2, "200")
    # AUCTION.add_item_image(2)
    #
    # AUCTION.add_new_auction("tv","electronics")
    # AUCTION.update_highest_bid(3, "300")
    # AUCTION.add_item_image(3)
    #
    # AUCTION.add_new_auction("lego","toys")
    # AUCTION.update_highest_bid(4, "400")
    # AUCTION.add_item_image(4)
    #
    # AUCTION.add_new_auction("baseball","sports")
    # AUCTION.update_highest_bid(5, "130")
    # AUCTION.add_item_image(5)
    #
    # AUCTION.add_new_auction("necklace","jewelry")
    # AUCTION.update_highest_bid(6, "120")
    # AUCTION.add_item_image(6)

    print("in-dex")
    resp = make_response(send_from_directory('public/html', 'index.html'))
    # add headers
    resp.headers['X-Content-Type-Options'] = 'nosniff'

    return resp

@app.route("/post-history")
def allHistory():
    auctions = AUCTION.get_all_auctions()
    auctionHistory = []
    # auth_token = request.cookies.get('auth_token')
    for item in auctions:
        print(item)
        auctionHistory.append({'_id': item['_id'],
                               'item_name': item['item_name'],
                               'category': item['category'],
                               'highest_bid': item['highest_bid'],
                               'image_name': item['image_name']
                               })
    resp = make_response(jsonify(auctionHistory))
    resp.mimetype = 'application/json'
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    return resp

@app.route("/post-history/<category>")
def historyHandler(category):
    # AUCTION.delete_all()
    print(category)
    auctions = AUCTION.get_auction_category(category)
    auctionHistory = []
    # auth_token = request.cookies.get('auth_token')
    for item in auctions:
        print(item)
        auctionHistory.append({'_id': item['_id'],
                               'item_name': item['item_name'],
                               'category': item['category'],
                               'highest_bid': item['highest_bid'],
                               'image_name': item['image_name']
                               })
    resp = make_response(jsonify(auctionHistory))
    resp.mimetype = 'application/json'
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    return resp

@app.route("/register", methods=['POST'])
def handleRegister():
    print(request.form, file=sys.stderr)
    username = request.form.get('username_reg')
    password = request.form.get('password_reg')
    return register(ACCOUNT, username, password)


@app.route("/login", methods=['POST'])
def handleLogin():
    print("handle login")
    username = request.form.get('username_login')
    password = request.form.get('password_login')
    return login(ACCOUNT, TOKEN, username, password)

@app.route('/authenticate',methods=['GET'])
def authenticate():
    tokenDb = Token()
    accounts = AuctionUsers()
    token = request.cookies.get('auth_token') 
    if token != None:   
        hashedToken = hashAuthToken(token)
    else:    
        hashedToken = None
        token = ''
    user = tokenDb.find_one_record({'tokenHash':hashedToken})
    if user == None:
        user = ''
    else:
        user = user['_id']
    return make_response(jsonify({'user':user,'token':token}))

@app.route("/<path:path>")
def getPage(path):
    print(path)
    root = '.'
    if not path.__contains__("public"):
        root = 'public'
    resp = make_response(send_from_directory(root,path))
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    return resp

@socket.route('/userAuctions')
def userAuctions(sock):
    auctions = AuctionPosts()
    startSig =  sock.receive()
    while True:
        sleep(1)
        data = auctions.getAllAuctionsAsList()
        sock.send(str(data))

@socket.route('/getAllAuctions')
def getAllAuctions(sock):
    auctions = AuctionPosts()
     
    while True:
        sleep(1)
        data = auctions.getAllAuctionsAsList()
        sock.send(data)

# @socket.route('/userAuctions')
# def userAuctions(sock):
#     t = Thread(target=handleAllAuctionsSocket)
#     startSig =  sock.receive()
    
    
@socket.route('/getAllAuctions/<path:path>')
def getAllAuctionsChat(sock,path):
    auctions = AuctionPosts()
    startSig =  sock.receive()
    while True:
        sleep(1)
        data = auctions.getAuctionsByCategoryAsList(path)
        sock.send(data)

def handleAllAuctionsSocket():
    auctions = AuctionPosts()
    newSock = Sock(app=app)
    sockets.append(newSock)  
    while True:
        sleep(1)
        data = auctions.getAllAuctionsAsList()
        newSock.send(jsonify(data))

if __name__ == "__main__":
    
    app.run('0.0.0.0',8080)
    
