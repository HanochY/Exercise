import secrets
from flask import Flask
from config.db import database


app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = secrets.token_urlsafe(32)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///KoolKluckerDB.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database.init_app(app)