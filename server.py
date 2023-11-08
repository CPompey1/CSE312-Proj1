import sys

from util.globals import ACCOUNT, TOKEN, AUCTION

from flask import Flask, request, make_response, send_from_directory

from util.login import login
from util.register import register

from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route("/")
def index():
    print("in-dex")
    resp = make_response(send_from_directory('public', 'index.html'))
    #add headers
    resp.headers['X-Content-Type-Options'] = 'nosniff'

    return resp
#
# @app.route("/post-history")
# def historyHandler():

# {
#             '_id': self.index,
#             'username': username,
#             'password': encrypt_password,
#         }
# @app.route("/post_auction_image")
# def handleImageUpload():
#     posts = AUCTION.getAllPost()
#     messageHistory = []
#     auth_token = request.cookies.get('auth_token')
# 
#     for ele in posts:
#         messageHistory.append({'_id': ele['_id'],
#                                'username': ele['username'],
#                                'title': ele['title'],
#                                'description': ele['description'],
#                                'likes': ele['likes'],
#                                'didCurrentUserLike': didCurrentUserLike(POSTS, TOKEN, ele['_id'], auth_token)
#                                })
#     resp = make_response(jsonify(messageHistory))
#     resp.mimetype = 'application/json'
#     resp.headers['X-Content-Type-Options'] = 'nosniff'
#     return resp
#     image = request.form.get('upload')
#
#     # Generate a secure filename for the uploaded image.
#     filename = secure_filename(image.filename)
#
#     # Define the path where you want to save the image.
#     upload_path = 'path/to/your/directory/' + filename
#
#     # Save the uploaded image to the specified path.
#     image.save(upload_path)


@app.route("/register", methods=['POST'])
def handleRegister():
    print(request.form,file=sys.stderr)
    username = request.form.get('username_reg')
    password = request.form.get('password_reg')
    return register(ACCOUNT,username,password)

@app.route("/login", methods=['POST'])
def handleLogin():
    print("handle login")
    username = request.form.get('username_login')
    password = request.form.get('password_login')
    return login(ACCOUNT,TOKEN,username,password)


@app.route("/<path:path>")
def getPage(path):
    root = '.'
    if not path.__contains__("public"):
        root = 'public'
    resp = make_response(send_from_directory(root, path))
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    return resp


if __name__ == "__main__":
    app.run('0.0.0.0', 8080)

