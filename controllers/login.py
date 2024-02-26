from flask import session
from config.db import database
from models.user import *
from utils.exceptions import *


def commit_login(username):
   session['user'] = username


def commit_logout():
   session.pop("user")


def validate_user_exists(username):
    if not check_user_exists(username):
        raise UserNotFoundError


def validate_password(username, password):
    if not get_password(username) == password:
        raise WrongPasswordError


def validate_password_confirmation(password, confirm_password):
    if not password == confirm_password:
        raise PasswordConfirmationError


def validate_username_available(username):
    if check_user_exists(username):
        raise UserAlreadyExistsError


def authenticate_login(username, password):
   validate_user_exists(username)
   validate_password(username, password)
   commit_login(username)


def authenticate_registration(username, password, confirm_password):
   validate_password_confirmation(password, confirm_password)
   validate_username_available(username)
   new_user = User(username, password)
   database.session.add(new_user)
   database.session.commit()
