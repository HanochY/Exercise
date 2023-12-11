import secrets

SECRET_KEY = secrets.token_urlsafe(32)
SQLALCHEMY_DATABASE_URI = "sqlite:///KoolKluckerDB.sqlite3"
SQLALCHEMY_TRACK_MODIFICATIONS = False