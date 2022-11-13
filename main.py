from flask import Flask

app = Flask(__name__)

import endpoint.root
import endpoint.user
import endpoint.content
import endpoint.chat

if __name__ =="__main__":
    app.run()
