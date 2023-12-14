from db_handler import database
from datetime import datetime

class Topic(database.Model):
   _id = database.Column('id', database.Integer, primary_key=True)
   name = database.Column(database.String(32))
   timestamp = database.Column(
        database.DateTime, nullable=False, default=datetime.now
   )

   def __init__(self, name):
      self.name = name
   