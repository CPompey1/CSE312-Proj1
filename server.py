from markupsafe import escape
import os
from flask import Flask,request,make_response, render_template,send_from_directory, jsonify
import sys
from util.database import  Account,Token, Posts
from util.globals import ACCOUNT,TOKEN,POSTS
from util.register import register
from util.response import htmlResponse
from util.login import login
from util.authToken import getTokenUsername




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
        response = make_response("post recieved", 200)
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
    
    app.run('0.0.0.0',8080,debug=True)
    
