from config.app import app

from routes.account_info import account_info_blueprint
from routes.forum import forum_blueprint
from routes.login import login_blueprint


app.register_blueprint(account_info_blueprint)
app.register_blueprint(forum_blueprint)
app.register_blueprint(login_blueprint)


with app.app_context():
    app.run(debug=True)