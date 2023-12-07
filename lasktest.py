from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "Aa123456"
admin = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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

class Comment_with_timestamp(Comment):
   timestamp = database.Column(database.String(32))
   def __init__(self, user, content, timestamp):
      super().__init__(user, content)
      self.timestamp = datetime.now()


def commit_login(username):
   session['user'] = username
   return redirect(url_for('forum'))

def create_user(username, password):
   new_user = User(username, password)
   database.session.add(new_user)
   database.session.commit()
   flash("User created!")

def handle_user_not_existing():
   flash('Credentials wrong!')
   return redirect(url_for("home"))

def handle_wrong_password():
   flash('Credentials wrong!')
   return redirect(url_for("home"))

def handle_user_already_exists():
   flash("User already exists!")
   return redirect(url_for('home'))

def handle_password_confirmation_failure():
   flash("Passwords do not match!")
   return redirect(url_for('home'))


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
   if database.session.query(User._id).filter_by(name=username).first():
      if database.session.query(User.password).filter_by(name=username).first()[0] == password:
         return commit_login(username)
      else:
         return handle_wrong_password()
   else:
      return handle_user_not_existing()

def authenticate_registration(username, password, confirm_password):
   if password == confirm_password:
      if database.session.query(User._id).filter_by(name=username).first() is None:
         create_user(username, password)
         return authenticate_login(username, password)
      else:
         return handle_user_already_exists()
   else:
      return handle_password_confirmation_failure()

def login_from_form():
   username, password = fetch_login_input()
   return authenticate_login(username, password)

def register_from_form():
   username, password, confirm_password = fetch_regsitration_input()
   return authenticate_registration(username, password, confirm_password)

@app.route('/', methods=['POST','GET'])
def home():
   if request.method == 'POST':
      if request.form["button"] == "register":
         return register_from_form()
      elif request.form["button"] == "login":
         return login_from_form()
   elif request.method == 'GET':
      return render_template("club.html")
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



@app.route('/forum', methods=['POST','GET'])
def forum():
   if session['user'] is not None:
      if request.method == 'POST':
         post_comment()
         return redirect(url_for("forum"))
      elif request.method == 'GET':
         return render_template("forum.html", username=session['user'], comments=Comment.query.all())
      else:
         return "ERROR: INVALID REQUEST"
   else:
      return redirect(url_for("home"))

@app.route('/account_info')
def account_info():
   if session['user'] is not None:
      return render_template("personal.html", username=session['user'])
   else:
      return redirect(url_for("home"))

@app.route('/admin')
def admin():
    return redirect(url_for("home"))

if __name__ == '__main__':
   with app.app_context():
      database.create_all()
   app.run(debug=True)