import flask
from routes.auth.login import *
from routes.auth.register import *
import os


# Create the application.
APP = flask.Flask(__name__)

@APP.route('/login', methods=['GET', 'POST'])
def login():
    return log_in()



@APP.route('/register', methods=['GET', 'POST'])
def register():
    if os.path.exists('user_files/admin/user.json'):
        return 'You are already registered'
        return redirect(url_for('index'), code=301)
    else:
        return register_user()


@APP.route('/', methods=['GET', 'POST'])
def index():
    if os.path.exists('user_files/admin/admin.json'):
        return 'You are logged in'
    else:
        return register_user()


if __name__ == '__main__':
    APP.debug=False
    APP.run()