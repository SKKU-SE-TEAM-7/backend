from __main__ import app
from flask import request,jsonify
from mongo.connection import db
from . import user
import random
import datetime
from bson.json_util import dumps

def find_recent():
    try:
        content_collection=db.content
        contents=content_collection.find({}).sort([('creation_time',1)]).limit(10)
        return contents
    except Exception as e:
        print(e)
        return False
def new_content(data):
    try:
        content_collection=db.content
        while True:
            if not content_collection.count_documents({"content-id":(id:=random.randint(1,10000000))}):break
        data['content-id'] = id
        data['image-url']= "url"
        data['targetMember']=int(data['targetMember'])
        email = user.getUser(data['token'])['email']
        data['writer']=email
        data['currentMember']=1
        data.pop('token',None)
        data['creation_time']=str(datetime.datetime.now())
        content_collection.insert_one(data)
        return True
    except Exception as e:
        print(e)
        return False
def get_content(content_id):
    try:
        content_collection=db.content
        if not (tar:=content_collection.find_one({"content-id":content_id})):
            data={}
            data['content-id'] = tar['content-id']
            data['image-url']= tar['image-url']
            data['detail']=tar['detail']
            data['writer']=tar['writer']
            return data
        return False
    except Exception as e:
        print(e)
        return False

@app.route('/content')
@app.route('/content/new',methods=['POST'])
def post_content():
    try:
        if new_content(request.form.to_dict()):
            return jsonify({"message":"upload success"})
        return jsonify({"message":"invalid password"})
    except Exception as e:
        return jsonify({'status':501,'error':str(e)})

@app.route('/content/get',methods=['GET'])
def get_content():
    try:
        data= get_content(request.args.get('content-id'))
        if data:
            return jsonify(data)
        return jsonify({"message":"get content fail"})
    except Exception as e:
        return jsonify({'status':501,'error':str(e)})


@app.route('/content/getRecent',methods=['GET'])
def get_recent():
    try:
        raw=find_recent()
        contents=[{key:item for key,item in x.items() if type(item) is str} for x in raw]
        return jsonify({'status':200,'list':contents})
    except Exception as e:
        return jsonify({'status':501,'message':str(e)})
@app.route('/content/join',methods=['GET'])
def join():
    return

