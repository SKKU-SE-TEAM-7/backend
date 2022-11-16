from pymongo import MongoClient,server_api
import certifi
#Atlas url
conn = MongoClient('mongodb+srv://skkuteam7:K6NyBGwj6i9tHn4R@cluster0.fiyvfqh.mongodb.net/?retryWrites=true&w=majority',server_api=server_api.ServerApi('1'),tlsCAFile=certifi.where())
db = conn.db
def createUser():
    db.create_collection("user")
    vexpr={
        "$jsonSchema" : {#이해를 돕기 위한 schema입니다. 실제로 적용 안됨
            "title" : "User_schema",
            "description" : "User schema contains email, password",
            "bsonType" : "object",
            "required" : ["user_email", "user_pw"],
            "properties" : {
                "User_email" : {
                    "bsonType" : "string",
                    "pattern" : "^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
                },
                "User_pw" : {
                    "bsonType" : "string",
                },
            }
        }
    }
    db.command({'collMod':"user","validator":vexpr,'validationLevel':'moderate'})
    db.user.create_index(['User_email',1],name='User_email',unique=True)

def createContent():
    db.create_collection("content")
    vexpr={#이해를 돕기 위한 schema입니다. 실제로 적용 안됨
        "$jsonSchema" : {
            "title" : "Content_Schema",
            "description" : "Content_Schema detail",
            "bsonType" : "object",
            "required" : ["title", "targetMember","dueDate","detail","currentMember","writer","participants"],
            "properties" : {
                "content-id":{
                    "bsonType":"integer",
                },
                "title" : {
                    "bsonType" : "string",
                    "pattern" : "^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
                },
                "targetMember" : {
                    "bsonType" : "integer",
                },
                "currentMember" : {
                    "bsonType" : "integer",
                },
                "detail" : {
                    "bsonType" : "string",
                },
            }
        }
    }
    db.content.create_index(['content-id',1],name='content-id',unique=True)
def createChat():
    #db.create_collection("chat")
    #이해를 돕기 위한 schema입니다. 실제로 적용 안됨
    vexpr={
        "$jsonSchema" : {
            "title" : "Content_Schema",
            "description" : "Content_Schema detail",
            "bsonType" : "object",
            "required" : ["title", "targetMember","dueDate","detail","currentMember","writer","participants"],
            "properties" : {
                "owner":{
                    "bsonType":"string",
                },
                "participant" : {
                    "bsonType" : "string",
                },
                "chat-id" : {
                    "bsonType" : "integer",
                },
                "chats" : {
                    "bsonType" : {
                        'time':'integer',
                        'sender':'email',
                        'text':'string'
                    }
                },
                "detail" : {
                    "bsonType" : "string",
                },
            }
        }
    }
if __name__=="__main__":
    createChat()