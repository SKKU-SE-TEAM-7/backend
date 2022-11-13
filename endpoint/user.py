from __main__ import app
from flask import request,jsonify,Response
from mongo.connection import db
from werkzeug.security import generate_password_hash,check_password_hash
import random

session={}


def getUser(token):
    print(session)
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
        print(e)
        return None


def new_user(email,pw):
    try:
        user_collection=db.user
        if user_collection.count_documents({'User_email':email})>0:
            print("exist email")
            return False
        user_collection.insert_one({'User_email':email,'User_pw':generate_password_hash(pw)})
        return True
    except Exception as e:
        print(e)
        return False


@app.route('/user')
@app.route('/user/login',methods=['POST'])
def login():
    try:
        email=request.form.get('user_email')
        password=request.form.get('user_password')
        if email and password and (token:=check_login(email,password)):
            return jsonify({"message":"login success","token":token})
        return jsonify({"message":"invalid password"})
    except Exception as e:
        return jsonify({'status':301,'error':str(e)})

@app.route('/user/register',methods=['POST'])
def register():
    try:
        email=request.form.get('user_email')
        password=request.form.get('user_password')
        if email and password and new_user(email,password):
            return jsonify({"message":"register success"})
        return jsonify({"message":"register fail"})
    except Exception as e:
        return jsonify({'status':301,'error':str(e)})




