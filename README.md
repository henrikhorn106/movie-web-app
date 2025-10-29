# Movie Web App

A simple Flask application to manage users and their favorite movies. It uses SQLite via SQLAlchemy and fetches movie details from the OMDb API.

## Features
- Create and list users
- View, add, update, and delete a user’s movies
- Fetch movie metadata (title, year, director, genre, poster) from OMDb by title and year
- Basic HTML templates and styling

## Requirements
- Python 3.13
- virtualenv
- Installed packages:
  - Flask
  - Flask-SQLAlchemy
  - Requests
  - Jinja2
  - Werkzeug
  - Click
  - SQLAlchemy
- OMDb API key

## Setup

1) Clone the repository and enter the project directory.
2) Create and activate a virtual environment
3) Install dependencies
4) Set your OMDb API key as an environment variable (replace YOUR_KEY)

Restart your terminal or re-activate the virtualenv if needed so the variable is available.

5) Initialize the database (on first run the app will create tables automatically).

## Running the App
bash python app.py

The server starts on http://127.0.0.1:5000

## Usage
- Home page displays all users and a form to add a new user.
- Click “View Movies” for a user to manage that user’s movie list.
- Add a movie by entering Title and Year. The app queries OMDb and stores details.

## Project Structure
- templates/: HTML templates
- static/: CSS assets
- data/: SQLite database storage
- app.py: Flask app and routes
- models.py: SQLAlchemy models
- data_manager.py: Data access layer

## Notes
- Ensure the OMDb API key is valid; adding a movie requires an external request.
- For local development, SQLite database is stored under data/movies.db.
- If you change models, delete the existing database file to recreate tables, or use migrations.