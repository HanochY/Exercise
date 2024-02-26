from flask import redirect, url_for, Blueprint,\
                  render_template, request, session, flash
from config.app import app
from controllers.login import *
from utils.exceptions import *


login_blueprint = Blueprint("login_blueprint", __name__)


@login_blueprint.route('/', methods=['POST', 'GET'])
def home():
   if 'user' in session:
      commit_logout()
   if request.method == 'POST':
      if request.form["button"] == "register":
         try:
            username = request.form["register_username"]
            password = request.form["register_password"]
            confirm_password = request.form["confirm_register_password"]
            authenticate_registration(username, password, confirm_password)
         except (PasswordConfirmationError, UserAlreadyExistsError) as error:
            flash(error.message)
         else:
            flash("User created!")
         finally:
            return redirect(url_for('login_blueprint.home'))
      elif request.form["button"] == "login":
         try:
            username = request.form["login_username"]
            password = request.form["login_password"]
            authenticate_login(username, password)
         except (UserNotFoundError, WrongPasswordError) as error:
            flash(error.message)
            return redirect(url_for('login_blueprint.home'))
         else:
            return redirect(url_for('forum_blueprint.forum'))
   elif request.method == 'GET':
      return render_template("login.html")
   else:
      return "ERROR: INVALID REQUEST"

