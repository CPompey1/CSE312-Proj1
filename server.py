from markupsafe import escape
import os,json
from flask import Flask,request,make_response, render_template,send_from_directory, jsonify
import sys
from util.database import  Account,Token, Posts
from util.globals import ACCOUNT,TOKEN,POSTS
from util.register import register
from util.response import htmlResponse
from util.login import login
from util.authToken import getTokenUsername
from util.like import like




app = Flask(__name__)

@app.route("/")
def handleIndex():
    return htmlResponse("public","index.html",200)

@app.route("/register", methods=['POST'])
def handleRegister():
    print(request.form,file=sys.stderr)
    username = request.form.get('username_reg')
    password = request.form.get('password_reg')
    return register(ACCOUNT,username,password)

@app.route("/login", methods=['POST'])
def handleLogin():
    print(request.form,file=sys.stderr)
    username = request.form.get('username_login')
    password = request.form.get('password_login')
    return login(ACCOUNT,TOKEN,username,password)

@app.route("/post-message", methods=['POST'])
def handlePost():
    if(request.method == 'POST'):
        title = request.get_json().get('title')
        description = request.get_json().get('description')
        print("title: %s\ndescription: %s" %(title,description), file=sys.stderr)
        #do database stuff
        authToken = request.cookies.get('auth_token')
        username = getTokenUsername(TOKEN,authToken)
        if username == None: username = 'Guest'
        res = POSTS.createPosts(username,title,description)
        response = make_response("post received", 200)
        return response
    
@app.route('/username', methods=['GET'])
def handleUsername():
    authToken = request.cookies.get('auth_token')
    print(request.cookies.get('auth_token'), file=sys.stderr)
    verifyTokenResult = getTokenUsername(TOKEN,authToken)
    if verifyTokenResult is not None:
        responseBody = {"username": verifyTokenResult}
    else:
        responseBody = {'username': 'Guest'}
    payload = jsonify(responseBody)
    resp = make_response(payload,200)
    return resp

@app.route('/post-history',methods=['GET'])
def postHistory():
    posts = POSTS.getAllPost()
    messageHistory = []
    for ele in posts: 
        messageHistory.append({'_id':ele['_id'],
                               'username':ele['username'],
                               'title':ele['title'],
                               'description':ele['description']})
    resp = make_response(jsonify(messageHistory))
    resp.mimetype = 'application/json'
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    return resp

@app.route('/like', methods=['POST'])
def handleLike():
    if request.method == 'POST':
        authToken = request.cookies.get('auth_token')
        username = getTokenUsername(TOKEN, authToken)
        message_id = request.get_json()         # what exactly is message_id getting?
        #message_id = message_id[:-1]
        #message_id = message_id[1:]            # maybe message_id is \message_id\  (see functions.js-82)
        print("message Id: " + str(message_id))     #print is never seen, function on line 88 is called tho
        if username is None:
            return
        res = like(username, message_id, POSTS)
        response = make_response("post liked", 200)
        return response

@app.route("/<path:path>")
def getPage(path):
    print(path)
    root = '.'
    if not path.__contains__("public"):
        root = 'public'
    resp = make_response(send_from_directory(root,path))
    resp.headers['X-Content-Type-Options'] = 'nosniff'

    return resp


        

if __name__ == "__main__":
    
    app.run('0.0.0.0',8080,debug=True)      #8090
    
