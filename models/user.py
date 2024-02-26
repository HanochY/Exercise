from config.db import database


class User(database.Model):
   _id = database.Column('id', database.Integer, primary_key=True)
   name = database.Column(database.String(32))
   password = database.Column(database.String(32))

   def __init__(self, name, password):
      self.name = name
      self.password = password
   
def get_password(username):
   return database.session.query(User.password)\
         .filter_by(name=username).first()[0]

def check_user_exists(username):
    return bool(database.session.query(User._id).
                filter_by(name=username).first())
