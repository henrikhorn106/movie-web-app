from models import db, User, Movie

class DataManager:
    """
    Handles user and movie-related data management operations.

    :ivar db: Database session used to interact with the database.
    :type db: SQLAlchemy
    """
    def create_user(self, name, email):
        """
        Creates and saves a new user to the database.

        :param username: The username for the new user.
        :type username: str
        :param email: The email address for the new user.
        :type email: str
        :return: The newly created user instance.
        :rtype: User
        """
        user = User(name=name, email=email)
        db.session.add(user)
        db.session.commit()
        return user

    def get_users(self):
        """
        Fetches all user records from the database.

        :return: A list of user records retrieved from the database.
        :rtype: list
        """
        return User.query.all()

    def get_movies(self, user_id):
        """
        Fetches a list of movies associated with a specific user.

        :param user_id: The ID of the user whose associated movies are to be fetched.
        :type user_id: int
        :return: A list of movies associated with the given user.
        :rtype: list
        """
        return Movie.query.filter_by(user_id=user_id).all()

    def add_movie(self, movie):
        """
        Adds a new movie to the database.

        :param movie: A movie instance to be added to the database.
        :return: The movie instance that was added to the database.
        """
        movie = Movie()
        db.session.add(movie)
        db.session.commit()
        return movie

    def update_movie(self, movie_id, new_title):
        """
        Updates the title of a movie in the database identified by the given movie ID
        with the provided new title.

        :param movie_id: The ID of the movie to be updated.
        :type movie_id: int
        :param new_title: The new title to assign to the movie.
        :type new_title: str
        :return: None
        """
        movie = Movie.query.filter_by(id=movie_id).first()
        movie.title = new_title
        db.session.commit()

    def delete_movie(self, movie_id):
        """
        Deletes a movie from the database based on its unique identifier.

        :param movie_id: The unique identifier of the movie to be deleted
        :type movie_id: int
        :return: None
        """
        movie = Movie.query.filter_by(id=movie_id).first()
        db.session.delete(movie)
