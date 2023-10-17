from flask import Flask
from flask import request
from flask import make_response
import subprocess

import hashlib

app = Flask(__name__)

# user1 password is password1
creds = {'1':['user1','7c6a180b36896a0a8c02787eeafb0e4c','My S3cret Phrase'], '2':['admin','ad58e137c3c6180ffae010bd11bb2f6b','P3rson@l Phrase']}

def validate_request(session,requested_asset):
    if session == creds[requested_asset][1]:
        return 'Valid'
    else:
    	return 'Not Valid'


@app.route('/')
def index():
    return '''
        <b>WELCOME TO THE IDOR ACCOUNT SYSTEM</b>
	<form action="/login" method="GET">
	  <label for="Username">Username:</label><br>
	  <input type="text" id="username" name="username" value="username"><br>
	  <label for="Password">Password:</label><br>
	  <input type="text" id="password" name="password" value="password"><br><br>
	  <input type="submit" value="Submit">
	</form> 
	'''
	
#Protected
@app.route('/account_secret_phrase', methods=['GET'])
def account_secret_phrase():
    id_val = request.args.get('id')
    session = request.args.get('session')
    if validate_request(session,id_val) == 'Valid':
        return "Welcome " + creds[id_val][0] + "!\nYour secret phrase is " + creds[id_val][2]
    else:
    	return "Access Denied"

#Protected
@app.route('/account_password', methods=['GET'])
def account_page_password():
    id_val = request.args.get('id')
    session = request.args.get('session')
    if validate_request(session,id_val):
        return "Welcome " + creds[id_val][0] + "!\nYour password hash is " + creds[id_val][1]
    else:
    	return "Access Denied"

#Public
@app.route('/account_user', methods=['GET'])
def account_page_username():
    id_val = request.args.get('id')
    return "Welcome " + creds[id_val][0] + "!\The username is " + creds[id_val][0]

@app.route('/login', methods=['GET'])
def login():
    user = request.args.get('username')
    password = request.args.get('password')
    password = hashlib.md5(password.encode())
    password = password.hexdigest()
    print(user + " " + password)
    for cred in creds:
        user_stored = creds[cred][0]
        print(user_stored)
        password_stored = creds[cred][1]
        print(password_stored)
        if user_stored == user:
            if password_stored == password:
                resp = make_response()
                resp.set_cookie("session",password)
                return "Access Granted. If you aren't automatically redirected, <a href=/account_secret_phrase?id=" + cred + "&session=" +password+">click here!</a>"
            else:
                return "Login Failed"
        else:
            return "Login Failed"
    return "Login Failed"


app.run(host='0.0.0.0', port=8181)