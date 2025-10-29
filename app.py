"""
A movie management application using Flask.

This script sets up a web application for managing users and their favorite
movies. The application leverages Flask for routing, SQLAlchemy for database
handling, and integrates with the OMDb API to fetch movie details. It includes
routes to display, create, update, and delete users as well as their associated
movies.
"""
import os

import requests
from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect

from data_manager import DataManager
from models import db, Movie

# Load .env file
load_dotenv()

# Access API key
api_key = os.environ.get('OMBD_API_KEY')

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Link the database and the app

data_manager = DataManager()  # Create an object of your DataManager class


@app.route('/', methods=['GET'])
def index():
    """
    Handles the root endpoint of the application.

    This function retrieves the list of users through the data_manager and
    renders the 'index.html' template with the provided user data.

    :return: Rendered HTML page populated with the list of users
    """
    try:
        users = data_manager.get_users()
    except IOError as e:
        print("An IOError occurred: ", str(e))

    return render_template('index.html', users=users)


@app.route('/users')
def list_users():
    """
    Retrieves the list of users and returns them as a string.

    :return: A string representation of the list of users
    """
    try:
        users = data_manager.get_users()
    except IOError as e:
        print("An IOError occurred: ", str(e))

    return str(users)  # Temporarily returning users as a string


@app.route('/users', methods=['POST'])
def create_user():
    """
    When the user submits the add user form, a POST request is made.
    The server receives the new user info, adds it to the database,
    then redirects back to /.

    :return: Redirect to the root endpoint
    """
    name = request.form['name']
    email = request.form['email']
    try:
        data_manager.create_user(name, email)
    except IOError as e:
        print("An IOError occurred: ", str(e))
    return redirect("/")


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def get_movies(user_id):
    """
    When you click on a user name, the app retrieves that user’s
    list of favorite movies and displays it.

    :return: Rendered HTML page populated with the list of movies
    """
    try:
        user = data_manager.get_user(user_id)
        movies = data_manager.get_movies(user_id)
    except IOError as e:
        print("An IOError occurred: ", str(e))

    return render_template('movies.html', movies=movies, user=user)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    """
    Add a new movie to a user’s list of favorite movies.

    :return: Redirect to the movies endpoint for the specified user
    """
    title = request.form['title']
    year = request.form['year']

    try:
        res = requests.get("https://www.omdbapi.com/", params={
            'apikey': api_key,
            't': title,
            'y': year
        }, timeout=5)
        data = res.json()
    except requests.exceptions.Timeout:
        return "Timeout error"
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

    if 'Error' in data:
        return f"Error: {data['Error']}"

    movie = Movie(
        title=data['Title'],
        year=data['Year'],
        director=data['Director'],
        genre=data['Genre'],
        poster=data['Poster'],
        user_id=user_id
    )

    try:
        data_manager.add_movie(movie)
    except IOError as e:
        print("An IOError occurred: ", str(e))

    return redirect(f"/users/{user_id}/movies")


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    """
    Modify the title of a specific movie in a user’s list,
    without depending on OMDb for corrections.

    :return: Redirect to the movies endpoint for the specified user
    """

    try:
        data_manager.update_movie(movie_id, request.form['title'])
    except IOError as e:
        print("An IOError occurred: ", str(e))

    return redirect(f"/users/{user_id}/movies")


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """
    Remove a specific movie from a user’s favorite movie list.

    :return: Redirect to the movies endpoint for the specified user
    """
    try:
        data_manager.delete_movie(movie_id)
    except IOError as e:
        print("An IOError occurred: ", str(e))

    return redirect(f"/users/{user_id}/movies")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run()
