from flask import redirect, url_for, Blueprint,\
                  render_template, request, session, flash
from controllers.forum import *
from config.app import app
from utils.exceptions import *


forum_blueprint = Blueprint("forum_blueprint", __name__)


@forum_blueprint.route('/forum/', methods=['POST', 'GET'])
def forum():
   if 'user' not in session:
      return redirect(url_for("login_blueprint.home"))
   if request.method == 'POST':
      try:
         user = session['user']
         content = request.form["forum_comment"]
         topic_name = request.form["comment_topic"]
         
         post_comment(user, content, topic_name)
      except EmptyCommentContentError:
         pass
      finally:
         return redirect(url_for("forum_blueprint.forum"))
   elif request.method == 'GET':
      return render_template("forum.html", username=session['user'],
                          topics=Topic.query.all(),
                          comments=Comment.query.all())
   else:
      return "ERROR: INVALID REQUEST"

