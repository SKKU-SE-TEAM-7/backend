from __main__ import app
from flask import request,jsonify,Response
from mongo.connection import db
from werkzeug.security import generate_password_hash,check_password_hash
import random

@app.route('/chat')

@app.route('/chat/getList')
def getRoomList():
    return
@app.route('/chat/getChat',methods=['GET'])
def getChat():
    return

@app.route('/chat/sendChat',methods=['POST'])
def sendChat():
    return