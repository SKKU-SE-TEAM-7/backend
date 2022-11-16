from __main__ import app
from flask import request,jsonify,Response
from mongo.connection import db
from werkzeug.security import generate_password_hash,check_password_hash
import random
import smtplib
from email.mime.text import MIMEText

session={1:{'email':'test2222@skku.edu'}}

auth_code={}

user_info_key=['nickname','User_email']
user_schema=['User_email','nickname','accumulate-star','join-content']

def getUser(token):
    return session[int(token)]

def check_login(email,pw):
    try:
        user_collection=db.user
        if valid:=user_collection.find_one({'User_email':email}):
            if check_password_hash(valid.get("User_pw"),pw):
                while True:
                    if not session.get(token:=random.randint(10000000,100000000)):break
                session[token]={"email":email}
                #TO-DO: db에 token을 넣어서 새로 로그인하면 이전 token을 만료시켜야함....
                return token
            return None
    except Exception as e:
        return None




@app.route('/user')
@app.route('/user/login',methods=['POST'])
def login():
    try:
        email=request.form.get('user_email')
        password=request.form.get('user_password')
        if email and password and (token:=check_login(email,password)):
            return jsonify({"message":"login success","token":token}) ,200
        return jsonify({"message":"invalid password"}),201
    except Exception as e:
        return jsonify({'error':str(e)}),301

@app.route('/user/register',methods=['POST'])
def register():
    try:
        email=request.form.get('user_email')
        password=request.form.get('user_password')
        nickname=request.form.get('nickname')
        code=request.form.get('authcode')
        if not (auth_code.get(email) and auth_code[email]==int(code)):
            return jsonify({'message':'auth code'}),201
        user_collection=db.user
        if user_collection.count_documents({'User_email':email})>0:
            return jsonify({'message':'email already exist'}),202
        user_collection.insert_one({'User_email':email,'User_pw':generate_password_hash(password),'nickname':nickname,'accumulate-star':0,'star-count':0,'join-content':[]})
        return jsonify({"message":"register success"}),200
    except Exception as e:
        return jsonify({'error':str(e)}),301

@app.route('/user/getinfo',methods=['GET'])
def getinfo():
    try:
        email=request.args.get('email')
        raw=db.user.find_one({'User_email':email})
        if raw:
            result={k:v for k,v in raw.items() if k in user_schema}
            result['star']=round(raw['accumulate-star']/raw['star-count'],1) if not raw['star-count']==0 else 3.0
            return jsonify({'user_info':result}),200
        return jsonify({'message':"wrong email"}),201
    except Exception as e:
        return jsonify({'error':str(e)}),501
@app.route('/user/joinlist',methods=['GET'])
def getJoinList():
    try:
        email=getUser(request.args.get('token'))['email']
        result=db.user.find_one({'User_email':email}).get('join-content')
        if result!=None:
            return jsonify({'joinlist':result}),200
        return jsonify({'message':"wrong token"}),201
    except Exception as e:
        return jsonify({'error':str(e)}),501
@app.route('/user/givereview',methods=['GET'])
def giveReview():
    try:
        email=request.args.get('email')
        db.user.update_one({'User_email':email},{'$inc':{'accumulate-star':int(request.args.get('star')),'star-count':1}})
        return jsonify({'message':'review success'}),200
    except Exception as e:
        return jsonify({'error':str(e)}),501
@app.route('/user/authcode',methods=['GET'])
def authcode():
    try:
        email=request.args.get('user_email')
        if db.user_collection.count_documents({'User_email':email})>0:
            return jsonify({'message':'email already exist'}),201
        if not email.split('@')[1] in ['skku.edu','g.skku.edu']:
            return jsonify({'message':'not allowed domain'}), 202
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()      # say Hello
        smtp.starttls()  # TLS 사용시 필요
        smtp.login('smtp.seongyunlee@gmail.com', 'fazzrlmughkedjme')
        
        code=random.randint(100000,1000000)
        msg = MIMEText('가입 인증코드는 '+str(code)+" 입니다.")
        msg['Subject'] = '[SKKU TEAM 7] 인증번호 알림'
        msg['To'] = 'mader0708@gmail.com'
        smtp.sendmail('noreply.skkuTeam7@skku.edu', email, msg.as_string())
        
        smtp.quit()
        auth_code[email]=code
        return jsonify({'message': 'auth code send success'}),200
    except Exception as e:
        return jsonify({'error':str(e)}),501