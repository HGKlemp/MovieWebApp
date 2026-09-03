from models import db, User, Movie


class DataManager:
    """Handle database CRUD operations."""

    def create_user(self, name):
        """Create a new user."""
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()

    def get_users(self):
        """Return a list of all users."""
        return User.query.all()

    def get_movies(self, user_id):
        """Return all movies for a specific user."""
        return Movie.query.filter_by(user_id=user_id).all()

    def add_movie(self, movie):
        """Add a new movie to the database."""
        db.session.add(movie)
        db.session.commit()

    def update_movie(self, movie_id, new_title):
        """Update a movie by its id."""
        Movie.query.filter_by(id=movie_id).update({"name": new_title})
        db.session.commit()

    def delete_movie(self, movie_id):
        """Delete a movie by its id."""
        Movie.query.filter_by(id=movie_id).delete()
        db.session.commit()