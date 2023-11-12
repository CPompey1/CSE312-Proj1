from markupsafe import escape
import os,sys
from flask import Flask,request,make_response, render_template,send_from_directory, send_from_directory, jsonify
# from sock import Sock

from flask_sock import Sock
from util.database.auctionPosts import AuctionPosts
from time import sleep
from util.globals import ACCOUNT, TOKEN, AUCTION
from util.login import login
from util.register import register
from werkzeug.utils import secure_filename

app = Flask(__name__)
socket = Sock(app)

def start_list():
    AUCTION.add_new_auction("bentley","cars")
    AUCTION.update_highest_bid(1, "100")
    AUCTION.add_item_image(1)

    AUCTION.add_new_auction("skirt","clothes")
    AUCTION.update_highest_bid(2, "200")
    AUCTION.add_item_image(2)

    AUCTION.add_new_auction("tv","electronics")
    AUCTION.update_highest_bid(3, "300")
    AUCTION.add_item_image(3)

    AUCTION.add_new_auction("lego","toys")
    AUCTION.update_highest_bid(4, "400")
    AUCTION.add_item_image(4)

    AUCTION.add_new_auction("baseball","sports")
    AUCTION.update_highest_bid(5, "130")
    AUCTION.add_item_image(5)

    AUCTION.add_new_auction("necklace","jewelry")
    AUCTION.update_highest_bid(6, "120")
    AUCTION.add_item_image(6)

@app.route("/")
def index():
    resp = make_response(send_from_directory('public/html', 'index.html'))
    # add headers
    resp.headers['X-Content-Type-Options'] = 'nosniff'

    return resp

@app.route("/create_auction")
def create_auction_handler():
    resp = make_response(send_from_directory('public/html', 'create_auction.html'))
    # add headers
    resp.headers['X-Content-Type-Options'] = 'nosniff'

    return resp

@app.route("/auctions_won")
def auction_won_handler():
    resp = make_response(send_from_directory('public/html', 'auctions_won.html'))
    # add headers
    resp.headers['X-Content-Type-Options'] = 'nosniff'

    return resp

@app.route("/closed_auctions")
def closed_auctions_handler():
    resp = make_response(send_from_directory('public/html', 'closed_auctions.html'))
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
    # print(request.form, file=sys.stderr)
    username = request.form.get('username_reg')
    password = request.form.get('password_reg')
    return register(ACCOUNT, username, password)


@app.route("/login", methods=['POST'])
def handleLogin():
    print("handle login")
    username = request.form.get('username_login')
    password = request.form.get('password_login')
    return login(ACCOUNT, TOKEN, username, password)

@app.route("/<path:path>")
def getPage(path):
    # print(path)
    root = '.'
    if not path.__contains__("public"):
        root = 'public'
    resp = make_response(send_from_directory(root,path))
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    return resp

@socket.route('/getAllAuctions')
def getAllAuctions(sock):
    auctions = AuctionPosts()
    startSig =  sock.receive()
    while True:
        sleep(1)
        data = auctions.getAllAuctionsAsList()
        sock.send(data)
    
@socket.route('/getAllAuctions/<path:path>')
def getAllAuctionsCat(sock, path):
    auctions = AuctionPosts()
    startSig =  sock.receive()
    while True:
        sleep(1)
        data = auctions.getAuctionsByCategoryAsList(path)
        sock.send(data)
    

if __name__ == "__main__":
    # start_list()
    app.run('0.0.0.0',8080)
    
