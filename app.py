import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for

from data_manager import DataManager
from models import db, Movie

load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
data_manager = DataManager()


@app.route('/')
def index():
    """Display the start page with all users."""
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users')
def list_users():
    """Return a list of all users."""
    users = data_manager.get_users()
    return str(users)


@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user and redirect to the start page."""
    name = request.form.get('name')
    data_manager.create_user(name)
    return redirect('/')


@app.route('/users/<int:user_id>/movies')
def get_movies(user_id):
    """Display all movies for a specific user."""
    movies = data_manager.get_movies(user_id)
    return render_template('movies.html', movies=movies, user_id=user_id)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    """Create a new movie for a specific user."""
    title = request.form.get('name')

    url = "https://www.omdbapi.com/"
    params = {"apikey": OMDB_API_KEY, "t": title}
    response = requests.get(url, params=params, timeout=10)
    movie_data = response.json()
    if movie_data.get("Response") == "False":
        return "Movie not found", 404

    movie = Movie(
        name=movie_data.get("Title"),
        director=movie_data.get("Director"),
        year=movie_data.get("Year"),
        poster_url=movie_data.get("Poster"),
        user_id=user_id
    )
    data_manager.add_movie(movie)
    return redirect(url_for('get_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    """Update an existing movie and redirect to the movie list."""
    name = request.form.get('name')
    director = request.form.get('director')
    year = request.form.get('year')
    poster_url = request.form.get('poster_url')
    data_manager.update_movie(movie_id, name, director, year, poster_url)
    return redirect(url_for('get_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """Delete a movie and redirect to the movie list."""
    data_manager.delete_movie(movie_id)
    return redirect(url_for('get_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(error):
    """Display a custom page when a resource is not found."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)