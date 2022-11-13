from pymongo import MongoClient,server_api
import certifi
#Atlas url
conn = MongoClient('mongodb+srv://skkuteam7:K6NyBGwj6i9tHn4R@cluster0.fiyvfqh.mongodb.net/?retryWrites=true&w=majority',server_api=server_api.ServerApi('1'),tlsCAFile=certifi.where())
db = conn.db

