import flask
from routes.auth.login import *
from routes.auth.register import *
from flask_jwt_extended import jwt_required, JWTManager, unset_jwt_cookies, get_jwt_identity, get_jwt
from datetime import timedelta, datetime, timezone
from jwt.exceptions import ExpiredSignatureError
from routes.misc.add_proxy import *
from dotenv import load_dotenv
from routes.misc.dashboard import *
from waitress import serve

dotenv = load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
PORT = os.getenv('PORT')


APP = flask.Flask(__name__)
jwt = JWTManager(APP)

APP.config['SERVER_NAME'] = '0.0.0.0' + ':' + PORT
APP.config['APPLICATION_ROOT'] = '/'
APP.config['JWT_TOKEN_LOCATION'] = ['cookies']
APP.config['JWT_SECRET_KEY'] = SECRET_KEY
APP.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)


@APP.route('/login', methods=['POST', 'GET'])
def login():
    if os.path.exists('user_files/admin/admin.json'):
        return log_in()
    else:
        return redirect(url_for('register'), code=301)


@APP.route('/register', methods=['GET', 'POST'])
def register():
    if os.path.exists('user_files/admin/admin.json'):

        return render_template('auth/already_registered.html')
    else:
        return register_user()


@APP.route('/', methods=['GET', 'POST'])
def index():
    if 'csrf_access_token' in request.cookies:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))


@APP.route('/dashboard', methods=['GET', 'POST'])
@jwt_required()
def dashboard(instance=None):
    navbar_options = analyze_instances('user_files/instances.json')
    if instance is None:
        return render_template('dashboard.html', navbar_options=navbar_options)
    else:
        print(instance)
        return render_template('dashboard.html', navbar_options=navbar_options)



@APP.route('/add_proxy', methods=['GET', 'POST'])
def add_proxy():
    if 'csrf_access_token' in request.cookies:
        csrf_access_token = request.cookies['csrf_access_token']
        return proxy_add_new(csrf_access_token)
    else:
        return redirect(url_for('login'))


@APP.route('/please_wait', methods=['GET', 'POST'])
def please_wait():

    return render_template('misc/please_wait.html')


@APP.route('/end_of_process', methods=['GET', 'POST'])
def end_of_process():
    return redirect(url_for('dashboard'))


@APP.route('/logout', methods=['POST'])
def logout():
    resp = flask.make_response(flask.redirect(flask.url_for('login')))
    unset_jwt_cookies(resp)
    return resp


@jwt.unauthorized_loader
def my_invalid_token_callback():
    return redirect(url_for('login'))


@APP.errorhandler(ExpiredSignatureError)
def handle_expired_token_error():
    return redirect(url_for('login'))


@APP.errorhandler(401)
def unauthorized_error():
    return redirect(url_for('login'))


@APP.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response


if __name__ == '__main__':
    APP.debug = False
    APP.run(port=PORT, host='0.0.0.0')
    #serve(APP, port=PORT, host='0.0.0.0') # I will use this in production
