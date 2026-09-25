from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from models import Movie, User, db


class DataManager:
    """Handle database CRUD operations."""

    def create_user(self, name):
        """Create a new user."""
        try:
            new_user = User(name=name)
            db.session.add(new_user)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise

    def get_users(self):
        """Return a list of all users."""
        return User.query.all()

    def get_user(self, user_id):
        """Return one user or None when the ID does not exist."""
        return db.session.get(User, user_id)

    def get_movies(self, user_id):
        """Return all movies for a specific user."""
        return Movie.query.filter_by(user_id=user_id).all()

    def movie_title_exists(self, user_id, title):
        """Check for a title in a user's collection, ignoring case."""
        normalized_title = title.strip().lower()
        return (
            Movie.query.filter(
                Movie.user_id == user_id,
                func.lower(Movie.name) == normalized_title,
            ).first()
            is not None
        )

    def add_movie(self, movie):
        """Add a new movie to the database."""
        try:
            db.session.add(movie)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise

    def update_movie_rating(self, user_id, movie_id, rating):
        """Update only the personal rating of a user's movie."""
        try:
            movie = Movie.query.filter_by(
                id=movie_id,
                user_id=user_id,
            ).first()

            if movie is None:
                return False

            movie.rating = rating
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            raise

    def delete_movie(self, user_id, movie_id):
        """Delete a movie that belongs to the given user."""
        try:
            movie = Movie.query.filter_by(
                id=movie_id,
                user_id=user_id,
            ).first()

            if movie is None:
                return False

            db.session.delete(movie)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            raise
