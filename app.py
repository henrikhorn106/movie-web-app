import requests
from flask import Flask, request, render_template, redirect
from data_manager import DataManager
from models import db, Movie
import os
from dotenv import load_dotenv


# Load .env file
load_dotenv()

# Access API key
api_key = os.environ.get('OMBD_API_KEY')


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Link the database and the app. This is the reason you need to import db from models

data_manager = DataManager() # Create an object of your DataManager class


@app.route('/', methods=['GET'])
def index():
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users')
def list_users():
    users = data_manager.get_users()
    return str(users)  # Temporarily returning users as a string


@app.route('/users', methods=['POST'])
def create_user():
    """
    When the user submits the add user form, a POST request is made.
    The server receives the new user info, adds it to the database,
    then redirects back to /.
    """
    name = request.form['name']
    email = request.form['email']
    user = data_manager.create_user(name, email)
    return redirect("/")


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def get_movies(user_id):
    """
    When you click on a user name, the app retrieves that user’s
    list of favorite movies and displays it.
    """
    movies = data_manager.get_movies(user_id)
    return str(movies)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    """
    Add a new movie to a user’s list of favorite movies.
    """
    title = request.form['title']

    res = requests.get(f"https://www.omdbapi.com/", params={
        'apikey': api_key,
        't': title
    })
    data = res.json()

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
    db.session.add(movie)
    db.session.commit()

    return f"Movie {title} added successfully!"



@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    """
    Modify the title of a specific movie in a user’s list,
    without depending on OMDb for corrections.
    """
    pass


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """
    Remove a specific movie from a user’s favorite movie list.
    """
    pass


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run()
