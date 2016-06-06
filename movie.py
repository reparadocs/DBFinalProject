from MyORM import *
from flask import Flask, render_template, request, redirect, url_for
from models import *

app = Flask(__name__)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    db = MyORM('movie')
    if request.method == 'GET':
        return render_template('register.html')
    else:
        user = User([0, db.sanitize(request.form['username'])])
        user = db.insert(user)
        if user is None:
            return render_template('register.html')
        else:
            return redirect(url_for('index', user_id=user.rowid))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    db = MyORM('movie')

    if request.method == 'GET':
        return render_template('login.html')
    else:
        condition = 'USERNAME = "' + db.sanitize(request.form['username']) + '"'
        match = db.filter(User, condition)
        if len(match) > 0:
            return redirect(url_for('index', user_id=match[0].rowid))
        else:
            return render_template('login.html')

@app.route('/index/<int:user_id>/', methods=['GET'])
def index(user_id):
    db = MyORM('movie')
    user = db.get(User, user_id)

    if user is None:
        return redirect(url_for('home'))

    return render_template('index.html')

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/movie/<int:movie_id>/', methods=['GET'])
def movie(movie_id):
    db = MyORM('movie')
    movie = db.get(Movie, movie_id)

    if movie is None:
        return redirect(url_for('home'))

    ratings = db.execute('SELECT (U.username, U.rowid, R.rating) \
                            FROM Movie M JOIN Rating R ON R.movie = M.rowid \
                                JOIN User U ON U.rowid = R.user \
                            WHERE M.rowid = ' + str(movie.rowid) + ';')

    return render_template('movie.html', title=movie.title, img_url=movie.img_url, ratings=list(ratings))




if __name__ == '__main__':
    db = MyORM('movie')

    if not db.doesTableExist(User):
        db.createTable(User)

    app.run(debug=True,)