from flask import Flask, request, make_response, redirect, render_template, url_for
import hashlib
import pymongo
import os

mongoURL = os.environ['db_url']

app = Flask(__name__)


@app.route('/')
def index():
    return redirect('https://turtle84375.me')

@app.route('/login', methods=['POST'])
def login():
    client = pymongo.MongoClient(mongoURL)
    db = client["turtle84375-me"]
    col = db["users"]
	
    user = request.form['username'].lower()
    pwrd = request.form['password']
    pwrd = hashlib.sha256(pwrd.encode('utf-8')).hexdigest()
    query = { "username": user, "password": pwrd }
    for x in col.find(query):
        print(x)
        if x.get('banned'):
          return redirect('https://turtle84375.me/login?error=3')
        else:
          resp = make_response(render_template('success.html'))
          resp.set_cookie('auth', x.get('username'), domain='.turtle84375.me', max_age=10)
          if x.get('admin'):
            resp.set_cookie('admin', 'true', domain='.turtle84375.me', max_age=10)
          return resp
    else:
        return redirect('https://turtle84375.me/login?error=1')

@app.route('/register', methods=['POST'])
def register():
    client = pymongo.MongoClient(mongoURL)
    db = client["turtle84375-me"]
    col = db["users"]
	
    user = request.form['username'].lower()
    pwrd = request.form['password']
					 

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug='true')