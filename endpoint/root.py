from __main__ import app

@app.route('/')
def test():
    return 'root test success'