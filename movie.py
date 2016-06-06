from MyORM import *
from flask import Flask, render_template, request, redirect, url_for, make_response
from models import *
import json
import random
import os

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
    if user_id == 0:
        user_id = request.cookies.get('user_id')
        if user_id is None:
            user_id = 0
        else:
            user_id = str(user_id)
            return redirect(url_for('index', user_id=user_id))
    db = MyORM('movie')
    user = db.get(User, user_id)

    if user is None:
        return redirect(url_for('home'))
    resp = make_response(render_template('index.html', user_id = user_id))
    resp.set_cookie('user_id', str(user_id))
    return resp

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/movie/<int:movie_id>/', methods=['GET'])
def movie(movie_id):
    db = MyORM('movie')
    movie = db.get(Movie, movie_id)

    if movie is None:
        return redirect(url_for('home'))

    db.execute('SELECT U.username, U.rowid, R.rating \
                            FROM Movie M JOIN Rating R ON R.movie = M.rowid \
                                JOIN User U ON U.rowid = R.user \
                            WHERE M.rowid = ' + str(movie.rowid) + ';')
    ratings = db.cursor.fetchall()

    db.execute('SELECT AVG(R.rating) \
                            FROM Movie M JOIN Rating R ON R.movie = M.rowid \
                                JOIN User U ON U.rowid = R.user \
                            WHERE M.rowid = ' + str(movie.rowid) + ';')
    avg = db.cursor.fetchall()[0][0]
    return render_template('movie.html', title=movie.title, img_url=movie.img_link, ratings=list(ratings), avg_rating=avg)

@app.route('/user/<int:user_id>/', methods=['GET'])
def user(user_id):
    db = MyORM('movie')
    user = db.get(User, user_id)
    if user is None:
        return redirect(url_for('home'))

    db.execute('SELECT M.title, M.rowid, R.rating \
                            FROM Movie M JOIN Rating R ON R.movie = M.rowid \
                                JOIN User U ON U.rowid = R.user \
                            WHERE U.rowid = ' + str(user.rowid) + ';')
    ratings = db.cursor.fetchall()
    db.execute('SELECT AVG(R.rating) \
                            FROM Movie M JOIN Rating R ON R.movie = M.rowid \
                                JOIN User U ON U.rowid = R.user \
                            WHERE U.rowid = ' + str(user.rowid) + ';')
    avg = db.cursor.fetchall()[0][0]
    return render_template('user.html', username=user.username, ratings=list(ratings), avg_rating=avg)

@app.route('/get_movie/<int:user_id>/<int:rid>/', methods=['GET'])
def getMovie(user_id, rid):
    db = MyORM('movie')
    user = db.get(User, user_id)
    if user is None:
        return redirect(url_for('home'))
    db.execute('SELECT M.title, M.img_link, M.rowid \
                FROM Movie M WHERE M.rowid NOT IN ( \
                    SELECT N.rowid FROM Movie N JOIN Rating R ON R.movie = N.rowid \
                    JOIN User U ON U.rowid = R.user WHERE U.rowid = ' + str(user.rowid) + ');')
    movies = list(db.cursor.fetchall())
    if len(movies) < 1:
        print "No movies left"
        return json.dumps({'error': 'No Movies Left To Rate'})
    random.seed(rid)
    movie = random.choice(movies)
    return json.dumps({'title': movie[0], 'img_url': movie[1], 'movie_id': movie[2]})

@app.route('/rate/<int:user_id>/<int:movie_id>/', methods=['POST'])
def rateMovie(user_id, movie_id):
    db = MyORM('movie')
    user = db.get(User, user_id)
    movie = db.get(Movie, movie_id)
    if user is None or movie is None:
        return redirect(url_for('home'))
    rating  = Rating([0, user.rowid, movie.rowid, request.form['rating']])
    db.insert(rating)
    return json.dumps({'success': True})

@app.route('/get_recommendations/<int:user_id>/', methods=['GET'])
def recommendMovies(user_id):

    db = MyORM('movie')
    user = db.get(User, user_id)
    if user is None:
        return redirect(url_for('home'))
    db.execute('SELECT M.title, M.img_link, M.rowid \
                FROM Movie M WHERE M.rowid NOT IN ( \
                    SELECT N.rowid FROM Movie N JOIN Rating R ON R.movie = N.rowid \
                    JOIN User U ON U.rowid = R.user WHERE U.rowid = ' + str(user.rowid) + ');')
    movies = list(db.cursor.fetchall())
    if len(movies) < 4:
        print "No movies left"
        return json.dumps({'error': 'No Movies Left To Rate'})
    rec_movies = []
    rec_movies.append(random.choice(movies))
    rec_movies.append(random.choice(movies))
    rec_movies.append(random.choice(movies))
    rec_movies.append(random.choice(movies))
    movie_data = []
    for movie in rec_movies:
        movie_data.append({"title": movie[0], "img_url": movie[1], "movie_id": movie[2]})
    return json.dumps(movie_data)

if __name__ == '__main__':
    db = MyORM('movie')

    if not db.doesTableExist(User):
        db.createTable(User)

    app.run(debug=True,)