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

    c_app = Flask(__name__, '/static')
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


@app.route('/users')
def users():
    return render_template('users.html')


@app.route('/correspondence')
def correspondence():
    correspondence.get_threads()
    return render_template('correspondence.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/login_user', methods=['GET', 'POST'])
def login_user():
    if request.method == 'GET':
        return render_template('index.html')

    username = request.form['username']
    password = request.form['password']
    users.login(username, password)

    return redirect('/')


@app.route('/logout_user')
def logout_user():
    users.logout()
    return redirect('/')


@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'GET':
        return render_template('register.html')

    ret = users.register(request)
    if not ret:
        return redirect('/register_user')

    return redirect('/')


@app.route('/delete_user', methods=['POST'])
def delete_user():

    users.check_csrf_token(request.form['csrf_token'])

    # print(request.form)
    # ret = users.delete_user(request)
    # print(ret)

    return redirect('/logout_user')


@app.route('/delete_contact', methods=['POST'])
def delete_contact():
    users.check_csrf_token(request.form['csrf_token'])
    users.delete_contact(request.form['contact_id'])
    return redirect('/users')


@app.route('/get_users')
def get_users():
    users.check_csrf_token(request.form['csrf_token'])
    users.get_users()
    return


@app.route('/select_user', methods=['POST'])
def select_user():
    users.check_csrf_token(request.form['csrf_token'])
    users.select_user(request.form['contact_id'])
    return redirect('/users')


@app.route('/select_thread', methods=['POST'])
def select_thread():
    users.check_csrf_token(request.form['csrf_token'])
    correspondence.select_thread(request.form['thread_id'])
    return redirect('/correspondence')


@app.route('/new_thread', methods=['POST'])
def new_thread():
    print(request)
    print(request.form)
    print(request.form['csrf_token'])
    print(request.form['thread_name'])
    print(request.form.getlist('contacts'))
    users.check_csrf_token(request.form['csrf_token'])
    correspondence.new_thread(request.form['thread_name'], request.form.getlist('contacts'))
    return redirect('/correspondence')


@app.route('/new_message', methods=['POST'])
def new_message():
    users.check_csrf_token(request.form['csrf_token'])
    correspondence.new_message(request.form['message'])
    return redirect('/correspondence')


@app.route('/send_contact_request', methods=['POST'])
def send_contact_request():
    users.check_csrf_token(request.form['csrf_token'])
    contact_id = request.form['contact_id']
    users.send_request(int(contact_id))
    return redirect('/users')


@app.route('/cancel_contact_request', methods=['POST'])
def cancel_contact_request():
    users.check_csrf_token(request.form['csrf_token'])
    contact_id = request.form['contact_id']
    users.cancel_contact_request(int(contact_id))
    return redirect('/users')


@app.route('/answer_contact_request', methods=['POST'])
def answer_contact_request():
    users.check_csrf_token(request.form['csrf_token'])
    if 'accept' in request.form:
        users.accept_request(request.form['accept'])
    if 'decline' in request.form:
        users.decline_request(request.form['decline'])
    return redirect('/users')


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
import correspondence


if __name__ == '__main__':
    app.run()
