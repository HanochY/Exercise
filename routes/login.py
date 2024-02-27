from flask import redirect, url_for, Blueprint,\
                  render_template, request, session, flash, jsonify
from controllers.login import *
from utils.exceptions import *


login_blueprint = Blueprint("login_blueprint", __name__)


@login_blueprint.route('/', methods=['GET'])
def home():
   return jsonify(None)

@login_blueprint.route('/logout', methods=['POST'])
def logout():
   try:
      commit_logout()
   except Exception as error:
      return jsonify({"message": error.message}), 400
   else:
      return jsonify({"message": "Logged out!"}), 201


@login_blueprint.route('/register', methods=['POST'])
def register():
   try:
      username = request.json.get("username")
      password = request.json.get("password")
      confirm_password = request.json.get("confirm_password")
      authenticate_registration(username, password, confirm_password)
   except (PasswordConfirmationError, UserAlreadyExistsError) as error:
      return jsonify({"message": error.message}), 400
   else:
      return jsonify({"message": "User registered!"}), 201

@login_blueprint.route('/login', methods=['POST'])
def login():
   try:
      username = request.json.get("username")
      password = request.json.get("password")
      authenticate_login(username, password)
   except (UserNotFoundError, WrongPasswordError) as error:
      return jsonify({"message": error.message}), 400
   else:
      token = ""
      return jsonify({"message": "User logged in!", "token": token}), 201
