from config.db import database
from datetime import datetime


class Topic(database.Model):
   _id = database.Column('id', database.Integer, primary_key=True)
   name = database.Column(database.String(32))
   timestamp = database.Column(
        database.DateTime, nullable=False, default=datetime.now
   )

   def __init__(self, name):
      self.name = name

def get_topic_id_by_name(topic_name):
    return database.session.query(Topic._id)\
            .filter_by(name=topic_name).first()[0]

def check_topic_exists(topic_name):
    return bool(database.session.query(Topic._id).
                filter_by(name=topic_name).first())