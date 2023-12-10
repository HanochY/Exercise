from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import config


app = Flask(__name__)
app.secret_key = config.SECRET_KEY
admin = False
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
database = SQLAlchemy(app)


class User(database.Model):
   _id = database.Column('id', database.Integer, primary_key = True)
   name = database.Column(database.String(32))
   password = database.Column(database.String(32))
   def __init__(self, name, password):
      self.name = name
      self.password = password


class Comment(database.Model):
   _id = database.Column('id', database.Integer, primary_key = True)
   user = database.Column(database.String(32))
   content = database.Column(database.String(32))
   def __init__(self, user, content):
      self.user = user
      self.content = content


class UserNotFoundError(Exception):
    def __init__(self):
       self.message = 'User does not exist!'
        

class WrongPasswordError(Exception):
    def __init__(self):
       self.message = 'Incorrect password!' 


class UserAlreadyExistsError(Exception):
    def __init__(self):
       self.message = 'User already exists!' 


class PasswordConfirmationError(Exception):
    def __init__(self):
       self.message = 'Passwords do not match!'


def commit_login(username):
   session['user'] = username
   return redirect(url_for('forum'))


def create_user(username, password):
   new_user = User(username, password)
   database.session.add(new_user)
   database.session.commit()
   flash("User created!")


def handle_error(error_type):
    message = {
        "user_not_existing": "No such user.",
        "wrong_password": "Incorrect password. Please try again.",
        "user_already_exists": "This username is already taken. You can choose another one.",
        "password_confirmation_failure": "Passwords do not match.",
    }
    flash(message[error_type])
    return redirect(url_for("home"))


def fetch_login_input():
   username = request.form["login_username"]
   password = request.form["login_password"]
   return username, password


def fetch_regsitration_input():
   username = request.form["register_username"]
   password = request.form["register_password"]
   confirm_password = request.form["confirm_register_password"]
   return username, password, confirm_password


def validate_user_exists(username):
   if not database.session.query(User._id).filter_by(name=username).first():
      raise UserNotFoundError


def validate_password(username, password):
   if not database.session.query(User.password).filter_by(name=username).first()[0] == password:
      raise WrongPasswordError


def validate_password_confirmation(password, confirm_password):
   if not password == confirm_password:
      raise PasswordConfirmationError


def validate_username_available(username):
   if not database.session.query(User._id).filter_by(name=username).first() is None:
      raise UserAlreadyExistsError


def authenticate_login(username, password):
   try:
      validate_user_exists(username)
      validate_password(username, password)
      return commit_login(username)
   except (UserNotFoundError, WrongPasswordError) as error:
      flash(error.message)
      return redirect(url_for('home'))


def authenticate_registration(username, password, confirm_password):
   try:
      validate_password_confirmation(password, confirm_password)
      validate_username_available(username)
      create_user(username, password)
      return authenticate_login(username, password)
   except (PasswordConfirmationError, UserAlreadyExistsError) as error:
      flash(error.message)
      return redirect(url_for('home'))


def login_from_form():
   username, password = fetch_login_input()
   return authenticate_login(username, password)


def register_from_form():
   username, password, confirm_password = fetch_regsitration_input()
   return authenticate_registration(username, password, confirm_password)


@app.route('/', methods=['POST','GET'])
def home():
   if 'user' in session:
      session.pop('user')
   if request.method == 'POST':
      if request.form["button"] == "register":
         return register_from_form()
      elif request.form["button"] == "login":
         return login_from_form()
   elif request.method == 'GET':
      return render_template("login.html")
   else:
       return "ERROR: INVALID REQUEST"


def commit_comment_submission():
   user = session['user']
   content = request.form["forum_comment"]
   new_comment = Comment(user, content)
   database.session.add(new_comment)
   database.session.commit()


def validate_comment_content():
   content = request.form["forum_comment"]
   return content is not None 


def check_form_submitted_comment():
   return request.form["button"] == "submit"


def post_comment():
   if check_form_submitted_comment():
      if validate_comment_content():
         commit_comment_submission()


@app.route('/forum/', methods=['POST','GET'])
def forum():
   if 'user' in session:
      if request.method == 'POST':
         post_comment()
         return redirect(url_for("forum"))
      elif request.method == 'GET':
         return render_template("forum.html", username=session['user'], comments=Comment.query.all())
      else:
         return "ERROR: INVALID REQUEST"
   else:
      return redirect(url_for("home"))


@app.route('/account_info/')
def account_info():
   if 'user' in session:
      return render_template("personal.html", username=session['user'])
   else:
      return redirect(url_for("home"))


if __name__ == '__main__':
   with app.app_context():
      database.create_all()
   app.run(debug=True)