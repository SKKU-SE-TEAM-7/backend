from __main__ import app
from flask import request,jsonify,Response
from mongo.connection import db
from . import user
from datetime import datetime
from bson.json_util import dumps
@app.route('/chat')
@app.route('/chat/getlist',methods=['GET'])
def getRoomList():
    try:
        email=user.getUser(request.args.get('token'))['email']
        result=db.chat.find({'$or':[{'owner':email},{'participant':email}]})
        if result:
            chatList=[{'chat-id':x['chat-id'],'owner':x['owner'],'participant':x['participant'],'content-id':x['content-id']}for x in result]
        return jsonify({'chatList':chatList}),200
    except Exception as e:
        return jsonify({"error":str(e)}),501

@app.route('/chat/getchat',methods=['GET'])
def getChat():
    try:
        chat = db.chat.find_one({'chat-id':int(request.args.get('chat-id'))})
        if not user.getUser(request.args.get('token'))['email'] in [chat['owner'],chat['participant']]:
            return jsonify({'message':'invalid access'}),201
        info={'chat-id':chat['chat-id'],'owner':chat['owner'],'participant':chat['participant'],'chats':chat['chats'],'content-id':chat['content-id']}
        if chat:
            return jsonify({'chat-info':info}),200
    except Exception as e:
        return jsonify({'error':str(e)}),501
@app.route('/chat/sendchat',methods=['POST'])
def sendChat():
    try:
        chat = db.chat.find_one({'chat-id':int(request.args.get('chat-id'))})
        if not (email:=user.getUser(request.args.get('token'))['email']) in [chat['owner'],chat['participant']]:
            return jsonify({'message':'invalid access'}),201
        if chat:
            db.chat.update_one({'chat-id':int(request.args.get('chat-id'))},{'$push':{'chats':{'time':str(datetime.now()),'sender':email,'text':request.form.get('text')}}})
            return jsonify({'message':"send success"}),200
    except Exception as e:
        return jsonify({'error':str(e)}),501