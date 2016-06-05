from MyORM import *
from flask import Flask, render_template, request, redirect, url_for
from models import *

app = Flask(__name__)
db = MyORM('movie')

if not db.doesTableExist(User):
    db.createTable(User)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else: 
        user = User([0, request.form['username'])
        db.insert(user)
        return redirect(url_for('index'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        condition = 'USERNAME = "' + request.form['username'] + '"'
        match = db.filter(User, condition)
        if len(match) > 0:
            return redirect(url_for('index'))
        else:
            return render_template('login.html')

@app.route('/index/', methods=['GET'])
def index():
    return render_template('index.html')
