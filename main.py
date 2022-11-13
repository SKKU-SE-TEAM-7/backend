from flask import Flask

app = Flask(__name__)

import endpoint.root
import endpoint.user

if __name__ =="__main__":
    app.run()
