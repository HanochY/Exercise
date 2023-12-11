from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()

from user import User
from comment import Comment
from exceptions import *


def create_user(username, password):
    new_user = User(username, password)
    database.session.add(new_user)
    database.session.commit()


def commit_comment_submission(user, content):
    new_comment = Comment(user, content)
    database.session.add(new_comment)
    database.session.commit()


def get_user_password(username):
    return database.session.query(User.password)\
            .filter_by(name=username).first()[0]


def check_user_exists(username):
    return bool(database.session.query(User._id).
                filter_by(name=username).first())


def validate_user_exists(username):
    if not check_user_exists(username):
        raise UserNotFoundError


def validate_password(username, password):
    if not get_user_password(username) == password:
        raise WrongPasswordError


def validate_password_confirmation(password, confirm_password):
    if not password == confirm_password:
        raise PasswordConfirmationError


def validate_username_available(username):
    if check_user_exists(username):
        raise UserAlreadyExistsError