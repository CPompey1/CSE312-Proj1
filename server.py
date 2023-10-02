from markupsafe import escape
import os
from flask import Flask,request,make_response, render_template,send_from_directory

app = Flask(__name__)


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


        

if __name__ == "__main__":
    app.run('0.0.0.0',8080)
    
