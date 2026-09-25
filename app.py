import os

from dotenv import load_dotenv
from flask import abort, flash, Flask, redirect, render_template, request, url_for

from data_manager import DataManager
from models import Movie, db
from omdb_api import MovieNotFoundError, OMDbAPI, OMDbAPIError


load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")

if not OMDB_API_KEY:
    raise RuntimeError("OMDB_API_KEY is not set.")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "development-secret-key")

basedir = os.path.abspath(os.path.dirname(__file__))

database_path = os.path.join(basedir, "data", "movies.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
data_manager = DataManager()
movie_api = OMDbAPI(OMDB_API_KEY)


@app.route("/")
def index():
    """Display the start page with all users."""
    users = data_manager.get_users()
    return render_template("index.html", users=users)


@app.route("/users")
def list_users():
    """Return a list of all users."""
    users = data_manager.get_users()
    return str(users)


@app.route("/users", methods=["POST"])
def create_user():
    """Create a new user and redirect to the start page."""
    name = request.form.get("name", "").strip()
    if not name:
        flash("Please enter a user name.", "error")
        return redirect(url_for("index"))

    data_manager.create_user(name)
    flash(f"User {name} was created.", "success")
    return redirect(url_for("index"))


@app.route("/users/<int:user_id>/movies")
def get_movies(user_id):
    """Display all movies for a specific user."""
    user = data_manager.get_user(user_id)
    if user is None:
        abort(404)

    movies = data_manager.get_movies(user_id)
    return render_template(
        "movies.html",
        movies=movies,
        user=user,
        user_id=user_id,
    )


@app.route("/users/<int:user_id>/movies", methods=["POST"])
def add_movie(user_id):
    """Create a new movie for a specific user."""
    if data_manager.get_user(user_id) is None:
        abort(404)

    title = request.form.get("name", "").strip()
    if not title:
        flash("Please enter a movie title.", "error")
        return redirect(url_for("get_movies", user_id=user_id))

    if data_manager.movie_title_exists(user_id, title):
        flash("This movie is already in your collection.", "error")
        return redirect(url_for("get_movies", user_id=user_id))

    try:
        movie_data = movie_api.fetch_movie(title)
    except MovieNotFoundError as error:
        flash(str(error), "error")
        return redirect(url_for("get_movies", user_id=user_id))
    except OMDbAPIError as error:
        flash(str(error), "error")
        return redirect(url_for("get_movies", user_id=user_id))

    if data_manager.movie_title_exists(user_id, movie_data["name"]):
        flash("This movie is already in your collection.", "error")
        return redirect(url_for("get_movies", user_id=user_id))

    movie = Movie(
        name=movie_data["name"],
        director=movie_data["director"],
        year=movie_data["year"],
        poster_url=movie_data["poster_url"],
        rating=0.0,
        user_id=user_id,
    )

    data_manager.add_movie(movie)
    flash(f'{movie.name} was added.', "success")

    return redirect(url_for("get_movies", user_id=user_id))


@app.route(
    "/users/<int:user_id>/movies/<int:movie_id>/update",
    methods=["POST"],
)
def update_movie(user_id, movie_id):
    """Update only the personal rating of an existing movie."""
    try:
        rating = float(request.form.get("rating", ""))
    except ValueError:
        flash("Please enter a valid rating.", "error")
        return redirect(url_for("get_movies", user_id=user_id))

    if not 0 <= rating <= 10:
        flash("The rating must be between 0 and 10.", "error")
        return redirect(url_for("get_movies", user_id=user_id))

    if not data_manager.update_movie_rating(user_id, movie_id, rating):
        abort(404)

    flash("Rating updated.", "success")
    return redirect(url_for("get_movies", user_id=user_id))


@app.route(
    "/users/<int:user_id>/movies/<int:movie_id>/delete",
    methods=["POST"],
)
def delete_movie(user_id, movie_id):
    """Delete a movie and redirect to the movie list."""
    if not data_manager.delete_movie(user_id, movie_id):
        abort(404)

    flash("Movie deleted.", "success")
    return redirect(url_for("get_movies", user_id=user_id))


@app.errorhandler(404)
def page_not_found(_error):
    """Display a custom page when a resource is not found."""
    return render_template("404.html"), 404


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
