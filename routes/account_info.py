from flask import redirect, url_for, Blueprint,\
                  render_template, request, session, flash
from config.app import app
from utils.exceptions import *


account_info_blueprint = Blueprint("account_info_blueprint", __name__)


@account_info_blueprint.route('/account_info/')
def account_info():
   if 'user' in session:
      return render_template("personal.html", username=session['user'])
   else:
      return redirect(url_for("login_blueprint.home"))
