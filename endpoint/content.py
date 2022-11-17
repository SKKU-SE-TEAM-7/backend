from __main__ import app
from flask import request,jsonify
from mongo.connection import db
from . import user
import random
import datetime
import base64
import boto3





content_schema=['title','detail','targetMember','duedate','content-id','image-url','owner','currentMember']
ACCESS_KEY_ID = 'AKIA2LLNWSDK6NBEWXTL'
ACCESS_SECRET_KEY = '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'
BUCKET_NAME = 'skkuseteam7'

def uploadImage(data,format,fileid):
    print(data,format,fileid)
    if not (data and format and fileid): return ''
    s3 = boto3.resource('s3',aws_access_key_id=ACCESS_KEY_ID,aws_secret_access_key=ACCESS_SECRET_KEY)
    s3.Bucket(BUCKET_NAME).put_object(Key='static/image/'+fileid+"."+format, Body=base64.b64decode(data), ContentType='image/'+format)    
    return 'skkuseteam7.s3.ap-northeast-2.amazonaws.com/static/image/'+fileid+"."+format

@app.route('/content')
@app.route('/content/new',methods=['POST'])
def post_content():
    try:
        content_collection=db.content
        while True:
            if not content_collection.count_documents({"content-id":(id:=random.randint(1,10000000))}):break
        data=request.form.to_dict()
        data['content-id'] = id
        data['image-url']= "url"
        data['targetMember']=int(data['targetMember'])
        email = user.getUser(request.args.get('token'))['email']
        data['image-url'] = uploadImage(request.form.get('image'),request.form.get('imageformat'),str(id))
        data['owner']=email
        data['currentMember']=0
        data['participant']=[]
        del data['image']
        data['creation_time']=str(datetime.datetime.now())
        if content_collection.insert_one(data):
            return jsonify({"message":"upload success","data":{k:d for k,d in data.items() if type(d) is str}}),200
        return jsonify({"message":"upload fail"}),201
    except Exception as e:
        return jsonify({'error':str(e)}),501
@app.route('/content/get',methods=['GET'])
def get_content():
    try:
        raw=db.content.find_one({"content-id":int(request.args.get('content-id'))})
        email=user.getUser(request.args.get('token'))['email'] 
        if raw:
            data={k:v for k,v in raw.items() if k in content_schema}
            data['is_joined']= email in raw['participant']
            data['chat-id']=db.chat.find_one({"owner":data['owner'],"participant":email})['chat-id'] if data['is_joined'] else 0
            return jsonify({"content":data}),200
        return jsonify({"message":"invalid content id"}),201
    except Exception as e:
        return jsonify({'error':str(e)}),501


@app.route('/content/getRecent',methods=['GET'])
def get_recent():
    try:
        content_collection=db.content
        raw=content_collection.find({}).sort([('creation_time',1)]).limit(20)
        contents=[{key:item for key,item in x.items() if key in content_schema} for x in raw]
        return jsonify({'list':contents}),200
    except Exception as e:
        return jsonify({'message':str(e)}),501
@app.route('/content/join',methods=['GET'])
def join():
    try:
        email=user.getUser(request.args.get('token'))['email']
        joined=db.content.find_one({'content-id':int(request.args.get('content-id'))})
        if not joined:
            return jsonify({"message":"wrong content id"}),201
        if joined['currentMember']==joined['targetMember']:
            return jsonify({'message':"Exceed Member"}),201
        if email == joined['owner']:
            return jsonify({"message":"it is my own content"}),201
        if email in joined['participant']:
            return jsonify({'message':"already joined"}),201
        db.content.update_one({'content-id':int(request.args.get('content-id'))}, {"$push":{'participant':email},"$inc":{'currentMember':1}})
        while True:
            if not db.chat.count_documents({"chat-id":(id:=random.randint(1,10000000))}):break
        db.chat.insert_one({'owner':joined['owner'],'participant':email,'content-id':int(request.args.get('content-id')),'chats':[],'chat-id':id})
        db.user.update_one({'user_email':email},{'$push':{'join-content':request.args.get('content-id')}})
        return jsonify({"message":"join success"}),200
    except Exception as e:
        return jsonify({"error":str(e)}),502
@app.route('/content/canceljoin',methods=['GET'])
def canceljoin():
    try:
        email=user.getUser(request.args.get('token'))['email']
        joined=db.content.find_one({'content-id':int(request.args.get('content-id'))})
        if not joined:
            return jsonify({"message":"wrong content id"}),201
        if not email in joined['participant']:
            print(joined['participant'])
            return jsonify({'message':"not joined yet"}),202
        db.content.update_one({'content-id':int(request.args.get('content-id'))}, {"$pull":{'participant':email},"$inc":{'currentMember':-1}})
        db.chat.delete_one({'content-id':int(request.args.get('content-id'))})
        db.user.update_one({'user_email':email},{'$pull':{'join-content':int(request.args.get('content-id'))}})
        return jsonify({"message":"cancel join success"}),200
    except Exception as e:
        return jsonify({"error":str(e)}),502
@app.route('/content/search',methods=['GET'])
def search_content():
    try:
        keyword=request.args.get('keyword').replace('+',')(?=.*')
        raw=db.content.find({'$or':[{'title':{'$regex':'(?=.*'+keyword+')'}},{'detail':{'$regex':'(?=.*'+keyword+')'}}]}).limit(20)
        contents=[{key:item for key,item in x.items() if key in content_schema} for x in raw]
        return jsonify({'list':contents}),200
    except Exception as e:
        return jsonify({'message':str(e)}),501
