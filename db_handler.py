from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()

from user import User
from comment import Comment
from topic import Topic
from exceptions import *


def create_user(username, password):
    new_user = User(username, password)
    database.session.add(new_user)
    database.session.commit()


def commit_comment_submission(user, content, topic_id):
    new_comment = Comment(user, content, topic_id)
    database.session.add(new_comment)
    database.session.commit()


def commit_topic_creation(name):
    new_topic = Topic(name)
    database.session.add(new_topic)
    database.session.commit()


def get_user_password(username):
    return database.session.query(User.password)\
            .filter_by(name=username).first()[0]


def check_user_exists(username):
    return bool(database.session.query(User._id).
                filter_by(name=username).first())


def get_topic_id_by_name(topic_name):
    return database.session.query(Topic._id)\
            .filter_by(name=topic_name).first()[0]


def check_topic_exists(topic_name):
    return bool(database.session.query(Topic._id).
                filter_by(name=topic_name).first())