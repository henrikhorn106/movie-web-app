"""
A module for defining database models using Flask SQLAlchemy.

This module defines two primary models, `User` and `Movie`, representing
users and movies within a database for a movie management application.
The `User` model includes information about users of the system, while
the `Movie` model includes information about movies and their associated
users.

The module uses Flask SQLAlchemy for interfacing with the database.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """
    Represents a User model in the database.

    This class defines the structure and attributes of a user in the database,
    where each user has an ID, a unique name, and a unique email address. It serves
    as the ORM (Object-Relational Mapping) mapping for the 'user' table.

    :ivar id: Unique identifier for the user.
    :type id: int
    :ivar name: Unique name of the user.
    :type name: str
    :ivar email: Unique email address of the user.
    :type email: str
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

    def __str__(self):
        return self.username


class Movie(db.Model):
    """
    Represents a Movie entity in the database.

    This class is a database model for storing information about movies.
    Each movie has several properties, including its title, release year,
    director, genre, and an associated poster. Additionally, each movie
    is linked to a specific user.

    :ivar id: Unique identifier for the movie.
    :type id: int
    :ivar title: Title of the movie, must be unique and not null.
    :type title: str
    :ivar year: Release year of the movie, cannot be null.
    :type year: int
    :ivar director: Name of the movie's director, cannot be null.
    :type director: str
    :ivar genre: Genre of the movie, cannot be null.
    :type genre: str
    :ivar poster: Path or URL of the movie's poster, cannot be null.
    :type poster: str
    :ivar user_id: ID of the user associated with this movie, cannot be null.
    :type user_id: int
    """
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    director = db.Column(db.String(120), nullable=False)
    genre = db.Column(db.String(120), nullable=False)
    poster = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Movie {self.title}>'

    def __str__(self):
        return self.title
