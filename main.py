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


def authenticate_login(username, password):
   db_handler.validate_user_exists(username)
   db_handler.validate_password(username, password)
   commit_login(username)


def authenticate_registration(username, password, confirm_password):
   db_handler.validate_password_confirmation(password, confirm_password)
   db_handler.validate_username_available(username)
   db_handler.create_user(username, password)


def validate_comment_content():
   if request.form["forum_comment"] is None:
      raise EmptyCommentContentError


def check_form_submitted_comment():
   return request.form["button"] == "submit"


def fetch_comment_input():
   print('oo')
   content = request.form["forum_comment"]
   return content


def post_comment(user, content):
   validate_comment_content()
   db_handler.commit_comment_submission(user, content)


def login_from_form():
   username, password = fetch_login_input()
   authenticate_login(username, password)


def register_from_form():
   username, password, confirm_password = fetch_regsitration_input()
   authenticate_registration(username, password, confirm_password)


def post_comment_from_form():
   if check_form_submitted_comment():
      user = session['user']
      content = fetch_comment_input()
      post_comment(user, content)


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
   if request.form["button"] == "register":
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