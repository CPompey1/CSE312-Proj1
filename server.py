from datetime import datetime
from markupsafe import escape
import os,sys
from flask import Flask,request,make_response, render_template,send_from_directory, send_from_directory, jsonify
# from sock import Sock
from flask_sock import Sock
from util.database.auctionPosts import AuctionPosts
from time import sleep
from util.globals import ACCOUNT, TOKEN, AUCTION, USERS
from util.token import getUserByAuthToken, hashAuthToken
from util.register import register
from util.authToken import *
from util.database.users import AuctionUsers
from werkzeug.utils import secure_filename
from threading import *
import json
from util.app.timeString import timeLeft, isAuctionOver
from util.forms import auction_login,auction_register
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import time
from google_auth_oauthlib.flow import InstalledAppFlow
from email.mime.text import MIMEText
import base64
from util.email import create_message, send_message, get_gmail_service 
import secrets

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def getClientAddress():
    try:
        return request.headers['X-Forwarded-For'] 
    except:
        return None

app = Flask(__name__)
socket = Sock(app)
blockedIPs = {}

limiter = Limiter(
    getClientAddress,
    app=app,
    default_limits=["50 per 10 seconds"]
)

#block requests and adds ip to blocked ip list
@app.errorhandler(429)
def ratelimit_handler(error):
    ip = getClientAddress()
    if ip is None:
        return
    blockedIPs[ip] = time.time() 
    return "Too Many Requests", 429

@app.before_request
def checkBlocked():
    ip = getClientAddress()
    if ip is None:
        return
    if blockedIPs.get(ip) is not None:
        timeLeft = time.time() - blockedIPs[ip]
        if timeLeft > 30:
            del blockedIPs[ip]
        else:
            return "Too Many Requests", 429

@app.route("/")
def index():
    resp = make_response(send_from_directory('public/html', 'index.html'))
    # add headers
    resp.headers['X-Content-Type-Options'] = 'nosniff'

    return resp


@app.route("/verification_status")
def checkUserIsVerified():
    authtoken = request.cookies.get("auth_token")
    if(authtoken == None):
        return make_response(jsonify({"verified": False}),200)
     
    user = USERS.findUserByToken(authtoken)

    if user == None:
        return make_response(jsonify({"verified": False}),200)
    
    return make_response(jsonify({"verified": user['verified']}),200)

@app.route("/send_verification_email")
def send_email():
    #get email based on auth token
    authtoken = request.cookies.get("auth_token")
    user = USERS.findUserByToken(authtoken)
    email = user['email']
    sender = 'packetsniffers312@gmail.com'
    subject = 'Please Verify Your Email'
    verification_code = secrets.token_hex(10)
    body = render_template('public/html/email.html', verification_code=verification_code)
    
    # Send the email
    service = get_gmail_service()
    send_message(service, sender_email, recipient_email, subject, body)

    return 0


    
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
    authtoken = request.cookies.get("auth_token")
    # print(authtoken, sys.stderr)
    if(authtoken is None):
        return make_response("Please Login", 403)
    user = getUserByAuthToken(authtoken)
    if(user is None):
        return make_response("Please Login", 403)
    image_name = AUCTION.add_new_auction(title, description, starting_price, auction_end)
    # print(user,sys.stderr)
    AuctionPosts().insertAuction(user['_id'],title,description,image_name,float(starting_price),auction_end,'none')

    if upload:
        file_data = upload.read()

        file_path = f"{os.getcwd()}/public/image/auction_images/" + str(image_name) + ".jpg"
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
        # print(item)
        auctionHistory.append({'_id': item['_id'],
                               'item_title': item['item_title'],
                               'item_description': item['item_description'],
                               'highest_bid': item['highest_bid'],
                               'auction_end': timeLeft(item['auction_end']),
                               })
    # print(auctionHistory)
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

def authenticateLoc():
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
    return {'user':user,'token':token}

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
    # auctions = AuctionPosts()
    # startSig =  sock.receive()
    # while True:
    #     sleep(1)
    #     data = auctions.getUserAuctions('cris')
    #     sock.send(json.dumps(data))
    auctions = AuctionPosts()
    startSig = sock.receive()
    user = json.loads(startSig)
    print(startSig)
    while True:
        sleep(1)
        data = auctions.getUserAuctions(user['user'])
        print(data,file=sys.stderr)
        createdAuctions = []
        wonAuctions = []
        for i in data.get('Created Auctions'):
           createdAuctions.append({
               "_id": i['_id'],
               "username": i['username'],
               "title": i['title'],
               "description": i['description'],
               "imageUrl": str(i['imageUrl'])+'.jpg',
               "startingPrice": i['startingPrice'],
               "category": i['category'],
               "highestBid": i['highestBid'],
            #    "bids": i['bids'],
               "active": i['active'],
               "timeLeft": timeLeft(i['endTime'])
           }) 
        
        for i in data.get('Won Auctions'):
           wonAuctions.append({
               "_id": i['_id'],
               "username": i['username'],
               "title": i['title'],
               "description": i['description'],
               "imageUrl": str(i['imageUrl'])+'.jpg',
               "startingPrice": i['startingPrice'],
               "category": i['category'],
               "highestBid": i['highestBid'],
            #    "bids": i['bids'],
               "active": i['active'],
               "timeLeft": timeLeft(i['endDate'])
           }) 
        payload = {"Created Auctions": createdAuctions,
                   "Won Auctions": wonAuctions}
        
        sock.send(json.dumps(payload))

@socket.route('/getAllAuctions')
def getAllAuctions(sock):
    auctions = AuctionPosts()
    startSig = sock.receive()
    while True:
        sleep(1)
        data = auctions.getAllAuctions()
        # print(data,file=sys.stderr)
        createdAuctions = []
        wonAuctions = []
        for i in data.get('Created Auctions'):
           if isAuctionOver(i['endTime']):
               wonAuctions.append({
               "_id": i['_id'],
               "username": i['username'],
               "title": i['title'],
               "description": i['description'],
               "imageUrl": str(i['imageUrl'])+'.jpg',
               "startingPrice": i['startingPrice'],
               "category": i['category'],
               "highestBid": i['highestBid'],
            #    "bids": i['bids'],
               "active": i['active'],
           }) 
               
           else:
                createdAuctions.append({
                    "_id": i['_id'],
                    "username": i['username'],
                    "title": i['title'],
                    "description": i['description'],
                    "imageUrl": str(i['imageUrl'])+'.jpg',
                    "startingPrice": i['startingPrice'],
                    "category": i['category'],
                    "highestBid": i['highestBid'],
                    #    "bids": i['bids'],
                    "active": i['active'],
                    "timeLeft": timeLeft(i['endTime'])
                }) 
           
           
        payload = {"Created Auctions": createdAuctions,
                   "Won Auctions": wonAuctions}
        
        sock.send(json.dumps(payload))

@app.route('/post-bid', methods=['POST'])
def place_bid():
    #get correct auction, update current bid and send the data
    #javascript to create http request with needed data then send that the endpoint
    auction_id = request.form.get('auction_id')
    posted_bid = request.form.get('posted-bid')
    find_auction = AUCTIONPOSTS.getAuctionByValue('_id', int(auction_id))
    
    if find_auction != None:
        print(find_auction)
        print(float(posted_bid))
        # print(float(find_auction['highestBid']))
        print(float(find_auction['startingPrice'])) 
        
        if float(posted_bid) > float(find_auction['highestBid']) and float(posted_bid) >= float(find_auction['startingPrice']):

            token = request.cookies.get('auth_token')
            hashed_token = hashAuthToken(token)
            username = USERS.findUserByToken(hashed_token)

            # replaces highest bid on auction with the user and their bid
            AUCTIONPOSTS.updateBids(int(auction_id), username['_id'], float(posted_bid))

            # adds the bid to the user's dictionary of bids
            # USERS.postUsersBid(username['_id'], int(auction_id), float(posted_bid))
    else:
        print("Auction does not exist")

    resp = make_response(send_from_directory('public/html', 'index.html'))
    # add headers
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    return resp
    

if __name__ == "__main__":
    
    app.run('0.0.0.0',8080)
    
