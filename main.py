from flask import Flask


app = Flask(__name__)

import endpoint.user
import endpoint.root

if __name__ =="__main__":
    app.run()
