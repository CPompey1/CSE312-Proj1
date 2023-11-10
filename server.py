from markupsafe import escape
import os
from flask import Flask,request,make_response, render_template,send_from_directory
from flask_sock import Sock

app = Flask(__name__)
socket = Sock(app)

@app.route("/")
def index():
    print()
    resp = make_response(send_from_directory('public','index.html'))
    #add headers
    resp.headers['X-Content-Type-Options'] = 'nosniff'

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
@socket.route('/echo')
def echo(sock):
    while True:
        data = sock.receive()
        sock.send(data)
    
    
if __name__ == "__main__":
    
    app.run('0.0.0.0',8080)
    

