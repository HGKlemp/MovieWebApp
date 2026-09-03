import os

from flask import Flask, render_template, request, redirect, url_for

from data_manager import DataManager
from models import db, Movie

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
data_manager = DataManager()


@app.route('/')
def index():
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users')
def list_users():
    users = data_manager.get_users()
    return str(users)


@app.route('/users', methods=['POST'])
def create_user():
    name = request.form.get('name')
    data_manager.create_user(name)
    return redirect('/')


@app.route('/users/<int:user_id>/movies')
def get_movies(user_id):
    movies = data_manager.get_movies(user_id)
    return render_template('movies.html', movies=movies, user_id=user_id)

@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    movie = Movie(
        name=request.form.get('name'),
        director=request.form.get('director'),
        year=request.form.get('year'),
        poster_url=request.form.get('poster_url'),
        user_id=user_id
    )
    data_manager.add_movie(movie)
    return redirect(url_for('get_movies', user_id=user_id))




if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
