from datetime import datetime

from markupsafe import escape
import os,sys
from flask import Flask,request,make_response, render_template,send_from_directory, send_from_directory, jsonify
# from sock import Sock

from flask_sock import Sock
from util.database.auctionPosts import AuctionPosts
from time import sleep
from util.globals import ACCOUNT, TOKEN, AUCTION, USERS
from util.token import getUserByAuthToken
from util.register import register
from util.authToken import *
from util.database.users import AuctionUsers
from werkzeug.utils import secure_filename
from threading import *
import json
from util.app.timeString import timeLeft
from util.forms import auction_login,auction_register

app = Flask(__name__)
socket = Sock(app)

@app.route("/")

def index():
    resp = make_response(send_from_directory('public/html', 'index.html'))
    # add headers
    resp.headers['X-Content-Type-Options'] = 'nosniff'

    return resp

@app.route("/post_auction", methods=['POST'])
def new_auction():
    resp = make_response(send_from_directory('public/html', 'post_successful.html'))
    # add headers
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    title = request.form.get('title')
    description = request.form.get('description')
    upload = request.files['upload']
    starting_price = request.form.get('starting_price')
    auction_end_str = request.form.get('auction_end')
    auction_end = datetime.strptime(auction_end_str, '%Y-%m-%dT%H:%M')
    image_name = AUCTION.add_new_auction(title, description, starting_price, auction_end)
    authtoken = request.cookies.get("auth_token")
    if(authtoken is None):
        return make_response("Please Login", 403)
    user = getUserByAuthToken(authtoken)
    AuctionPosts().insertAuction(user['_id'],title,description,image_name,float(starting_price),auction_end,'none')

    if upload:
        file_data = upload.read()

        file_path = "/root/auction_images/" + str(image_name) + ".jpg"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'wb') as file:
            file.write(file_data)
            file.close()
    return resp

@app.route("/profile")
def handleProfile():
    resp = make_response(send_from_directory('public/html', 'post_new_auction.html'))
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
                               'item_title': item['item_title'],
                               'item_description': item['item_description'],
                               'highest_bid': item['highest_bid'],
                               'auction_end': timeLeft(item['auction_end'])
                               })
    print(auctionHistory)
    resp = make_response(jsonify(auctionHistory))
    resp.mimetype = 'application/json'
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    return resp


@app.route("/register", methods=['POST'])
def handleRegister():
    # print(request.form, file=sys.stderr)
    username = request.form.get('username_reg')
    password = request.form.get('password_reg')
    return auction_register(username, password)


@app.route("/login", methods=['POST'])
def handleLogin():
    username = request.form.get('username_login')
    password = request.form.get('password_login')
    return auction_login(username, password)

@app.route('/authenticate',methods=['GET'])
def authenticate():
    accounts = AuctionUsers()
    token = request.cookies.get('auth_token') 
    if token != None:   
        hashedToken = hashAuthToken(token)
    else:    
        hashedToken = None
        token = ''
    user = accounts.findUserByToken(hashedToken)
    if user == None:
        user = ''
    else:
        user = user['_id']
    return make_response(jsonify({'user':user,'token':token}))

@app.route("/<path:path>")
def getPage(path):
    # print(path)
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
        data = auctions.getUserAuctions('cris')
        sock.send(json.dumps(data))

@socket.route('/getAllAuctions')
def getAllAuctions(sock):
    auctions = AuctionPosts()
    startSig = sock.receive()
    while True:
        sleep(1)
        data = auctions.getAllAuctions()
        print(data,file=sys.stderr)
        createdAuctions = []
        wonAuctions = []
        for i in data.get('Created Auctions'):
           createdAuctions.append({
               "_id": i['_id'],
               "username": i['username'],
               "title": i['title'],
               "description": i['description'],
               "imageUrl": i['imageUrl'],
               "startingPrice": i['startingPrice'],
               "category": i['category'],
               #"highestBid": i['highestBid'],
               "bids": i['bids'],
               "active": i['active'],
               "timeLeft": timeLeft(i['endTime'])
           }) 
        
        for i in data.get('Won Auctions'):
           wonAuctions.append({
               "_id": i['_id'],
               "username": i['username'],
               "title": i['title'],
               "description": i['description'],
               "imageUrl": i['imageUrl'],
               "startingPrice": i['startingPrice'],
               "category": i['category'],
               #"highestBid": i['highestBid'],
               "bids": i['bids'],
               "active": i['active'],
               "timeLeft": timeLeft(i['endDate'])
           }) 
        payload = {"Created Auctions": createdAuctions,
                   "Won Auctions": wonAuctions}
        
        sock.send(json.dumps(payload))


# @socket.route('/userAuctions')
# def userAuctions(sock):
#     t = Thread(target=handleAllAuctionsSocket)
#     startSig =  sock.receive()
    

@socket.route('/ws')
def socket_reponse(ws):
    while True:
        sleep(1)
        auctions = AuctionPosts().getAllAuctionsAsList()
        updatedTimes = []
        for auction in auctions:
            updatedTimes.append({
                "auctionId": auction["_id"],
                "timeLeft": timeLeft(auction['endTime'])
            })
        ws.send(json.dumps(
            {"messageType": 'timerUpdate', 'updatedTimes': updatedTimes}))
    

if __name__ == "__main__":
    
    app.run('0.0.0.0',8080)
    
