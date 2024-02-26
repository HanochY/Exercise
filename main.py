from flask import Flask, redirect, url_for,\
                  render_template, request, session, flash
import config
from db_handler import database


app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = \
   config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = \
   config.SQLALCHEMY_TRACK_MODIFICATIONS
database.init_app(app)


import db_handler
from exceptions import *


INVALID_REQUEST_ERROR_MESSAGE = "ERROR: INVALID REQUEST"


def commit_login(username):
   session['user'] = username


def commit_logout():
   session.pop("user")


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
    if not db_handler.check_user_exists(username):
        raise UserNotFoundError


def validate_password(username, password):
    if not db_handler.get_user_password(username) == password:
        raise WrongPasswordError


def validate_password_confirmation(password, confirm_password):
    if not password == confirm_password:
        raise PasswordConfirmationError


def validate_username_available(username):
    if db_handler.check_user_exists(username):
        raise UserAlreadyExistsError


def authenticate_login(username, password):
   validate_user_exists(username)
   validate_password(username, password)
   commit_login(username)


def authenticate_registration(username, password, confirm_password):
   validate_password_confirmation(password, confirm_password)
   validate_username_available(username)
   db_handler.create_user(username, password)


def check_form_submitted_comment():
   return request.form["button"] == "comment"


def fetch_comment_input():
   content = request.form["forum_comment"]
   return content

def fetch_topic_input():
   content = request.form["comment_topic"]
   return content

def post_comment(user, content, topic_id):
   if content:
      db_handler.commit_comment_submission(user, content, topic_id)
   else:
      raise EmptyCommentContentError

def create_topic(name):
   if name:
      db_handler.commit_topic_creation(name)
   else:
      raise EmptyTopicNameError
   

def login_from_form():
   username, password = fetch_login_input()
   authenticate_login(username, password)


def register_from_form():
   username, password, confirm_password = fetch_regsitration_input()
   authenticate_registration(username, password, confirm_password)


def post_comment_from_form():
   user = session['user']
   content = fetch_comment_input()
   topic_name = fetch_topic_input()
   if not db_handler.check_topic_exists(topic_name):
      print('tttt')
      create_topic(topic_name)
   topic_id = db_handler.get_topic_id_by_name(topic_name)
   post_comment(user, content, topic_id)


def try_register():
   try:
      register_from_form()
   except (PasswordConfirmationError, UserAlreadyExistsError) as error:
      flash(error.message)
   else:
      flash("User created!")
   finally:
      return redirect(url_for('home'))


def try_login():
   try:
      login_from_form()
   except (UserNotFoundError, WrongPasswordError) as error:
      flash(error.message)
      return redirect(url_for('home'))
   else:
      return redirect(url_for('forum'))


def handle_home_post():
   if request.form["butto n"] == "register":
      return try_register()
   elif request.form["button"] == "login":
      return try_login()


def handle_home_get():
   return render_template("login.html")


def handle_forum_post():
   try:
      post_comment_from_form()
   except EmptyCommentContentError:
      pass
   finally:
      return redirect(url_for("forum"))


def handle_forum_get():
   return render_template("forum.html", username=session['user'],
                          topics=db_handler.Topic.query.all(),
                          comments=db_handler.Comment.query.all())


def handle_account_info_get():
   return render_template("personal.html", username=session['user'])


@app.route('/', methods=['POST', 'GET'])
def home():
   if 'user' in session:
      commit_logout()
   if request.method == 'POST':
      return handle_home_post()
   elif request.method == 'GET':
      return handle_home_get()
   else:
      return INVALID_REQUEST_ERROR_MESSAGE


@app.route('/forum/', methods=['POST', 'GET'])
def forum():
   if 'user' not in session:
      return redirect(url_for("home"))
   if request.method == 'POST':
      return handle_forum_post()
   elif request.method == 'GET':
      return handle_forum_get()
   else:
      return INVALID_REQUEST_ERROR_MESSAGE


@app.route('/account_info/')
def account_info():
   if 'user' in session:
      return handle_account_info_get()
   else:
      return redirect(url_for("home"))


if __name__ == '__main__':
   with app.app_context():
      database.create_all()
   app.run(debug=True)