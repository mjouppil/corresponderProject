from flask import Flask
from flask import redirect, render_template, request, make_response
from flask_bootstrap import Bootstrap
from os import getenv, path
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy


def create_app():
    basedir = path.abspath(path.dirname(__file__))
    env_dir = path.join(basedir, '.env')
    load_dotenv(env_dir)

    c_app = Flask(__name__)
    c_app.secret_key = getenv('SECRET_KEY')
    c_app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
    c_db = SQLAlchemy(c_app)
    c_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    Bootstrap(c_app)

    return c_app, c_db


app, db = create_app()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login_user', methods=['GET', 'POST'])
def login_user():
    if request.method == 'GET':
        return render_template('index.html')

    username = request.form['username']
    password = request.form['password']

    ret = users.login(username, password)

    return redirect('/')


@app.route('/logout_user')
def logout_user():
    users.logout()
    return redirect('/')


@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'GET':
        return render_template('register.html')

    print(request.form)

    ret = users.register(request)
    print(ret)

    if not ret:
        return redirect('/register_user')

    return redirect('/')


@app.route('/delete_user', methods=['POST'])
def delete_user():

    users.check_csrf_token(request.form['csrf_token'])

    print(request.form)
    ret = users.delete_user(request)
    print(ret)

    return redirect('/logout_user')


@app.route('/get_users')
def get_users():
    users.get_users()
    return


def get_contacts():
    return


def new_thread():
    return


def new_message():
    return


def get_threads():
    return


def get_messages():
    return


@app.route('/send_contact_request', methods=['POST'])
def send_contact_request():
    print(request)
    #user_id= request.form['user_id']
    contact_id = request.form['contact_id']
    # contact_token = request.form['contact_token']

    ret = users.send_request(int(contact_id))
    print(ret)

    return redirect('/')


@app.route('/answer_contact_request', methods=['POST'])
def answer_contact_request():

    if 'accept' in request.form:
        users.accept_request(request.form['accept'])
    if 'decline' in request.form:
        users.decline_request(request.form['decline'])

    return redirect('/')


@app.errorhandler(404)
def not_found():
    """Page not found."""
    return make_response(
        render_template("error.html"),
        404
     )


@app.errorhandler(400)
def bad_request():
    """Bad request."""
    return make_response(
        render_template("error.html"),
        400
    )


@app.errorhandler(500)
def server_error():
    """Internal server error."""
    return make_response(
        render_template("error.html"),
        500
    )


import users


if __name__ == '__main__':
    app.run()
