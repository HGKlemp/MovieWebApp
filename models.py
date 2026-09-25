from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    """Represent a user of the movie application."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Movie(db.Model):
    """Represent a movie belonging to a user."""
    __table_args__ = (
        db.UniqueConstraint("user_id", "name", name="uq_movie_user_title"),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100, collation="NOCASE"), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    poster_url = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=False, default=0.0)

    # Link Movie to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
