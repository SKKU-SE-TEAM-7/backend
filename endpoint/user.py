from __main__ import app

@app.route('/user')
def user():
    return 'test success'