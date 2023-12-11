from db_handler import database


class User(database.Model):
   _id = database.Column('id', database.Integer, primary_key=True)
   name = database.Column(database.String(32))
   password = database.Column(database.String(32))

   def __init__(self, name, password):
      self.name = name
      self.password = password