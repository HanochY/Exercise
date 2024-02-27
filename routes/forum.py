from flask import Blueprint, request, jsonify
from controllers.forum import *
from utils.exceptions import *


forum_blueprint = Blueprint("forum_blueprint", __name__)


@forum_blueprint.route('/get_comments/', methods=['GET'])
def forum():
   try:
      topics = list(map(lambda x: x.to_json(), Topic.query.all()))
      comments = list(map(lambda x: x.to_json(), Comment.query.all()))
      return jsonify({"topics": topics, "comments": comments})
   except Exception as error:
      return jsonify({"message": error.message}), 500

@forum_blueprint.route('/post_comment/', methods=['POST'])
def post_comment():
   try:
      user = request.json.get("username")
      content = request.json.get("comment_content")
      topic_name = request.json.get("comment_topic")
      post_comment(user, content, topic_name)
   except EmptyCommentContentError:
      return jsonify({"message": "Comment must have content!"}), 400
   else:
      return jsonify({"message": "Comment created!"}), 201

