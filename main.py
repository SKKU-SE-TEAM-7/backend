from flask import Flask

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


import endpoint.root
import endpoint.user
import endpoint.content
import endpoint.chat

if __name__ =="__main__":
    app.run(host="0.0.0.0",port=8080,debug=False)
