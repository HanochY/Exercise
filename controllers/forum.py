from flask import request
from config.db import database
from models.comment import *
from models.topic import *
from utils.exceptions import *

def check_form_submitted_comment():
   return request.form["button"] == "comment"


def post_comment(user, content, topic_name):
   if content:
      if not check_topic_exists(topic_name):
         create_topic(topic_name)
      topic_id = get_topic_id_by_name(topic_name)
      new_comment = Comment(user, content, topic_id)
      database.session.add(new_comment)
      database.session.commit()
   else:
      raise EmptyCommentContentError

def create_topic(name):
   if name:
      new_topic = Topic(name)
      database.session.add(new_topic)
      database.session.commit()
   else:
      raise EmptyTopicNameError
