from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    """Represent a user of the movie application."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Movie(db.Model):
    """Represent a movie belonging to a user."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    poster_url = db.Column(db.String(500), nullable=False)

    # Link Movie to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)