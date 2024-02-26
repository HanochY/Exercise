from config.db import database
from datetime import datetime


class Comment(database.Model):
   _id = database.Column('id', database.Integer, primary_key=True)
   user = database.Column(database.String(32))
   content = database.Column(database.String(32))
   topic_id = database.Column(database.Integer)
   timestamp = database.Column(
        database.DateTime, nullable=False, default=datetime.now
   )

   def __init__(self, user, content, topic_id):
      self.user = user
      self.content = content
      self.topic_id = topic_id

