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

    if not request.form['username'] or len(request.form['username']) < 3:
        toast_text = 'Username missing or too short (minimum 3 characters).'
        return render_template('register.html', toastText=toast_text)
    if not request.form['username'] or len(request.form['username']) < 3:
        toast_text = 'Password missing or too short (minimum 3 characters).'
        return render_template('register.html', toastText=toast_text)

    ret = users.register(request)
    if not ret:
        toast_text = 'Registering failed.'
        return render_template('register.html', toastText=toast_text)

    return redirect('/')


@app.route('/delete_user', methods=['POST'])
def delete_user():
    users.check_csrf_token(request.form['csrf_token'])
    return redirect('/logout_user')


@app.route('/delete_contact', methods=['POST'])
def delete_contact():
    users.check_csrf_token(request.form['csrf_token'])
    users.delete_contact(request.form['contact_id'])
    alias = request.form['alias']
    toast_text = f'{alias} removed from contacts.'
    return render_template('users.html', toastText=toast_text)


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
    users.check_csrf_token(request.form['csrf_token'])
    if request.form['thread_name'] == "":
        toast_text = f"New thread is missing a name."
        return render_template('correspondence.html', toastText=toast_text)
    correspondence.new_thread(request.form['thread_name'], request.form.getlist('contacts'))
    toast_text = f"{request.form['thread_name']}-thread created"
    return render_template('correspondence.html', toastText=toast_text)


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
    alias = request.form['alias']
    toast_text = f'Contact request sent to {alias}.'
    return render_template('users.html', toastText=toast_text)


@app.route('/send_contact_request_token', methods=['POST'])
def send_contact_request_token():
    users.check_csrf_token(request.form['csrf_token'])
    users.send_request_by_token(request.form['contact_token'])
    toast_text = f'Contact request by token sent.'
    return render_template('users.html', toastText=toast_text)


@app.route('/cancel_contact_request', methods=['POST'])
def cancel_contact_request():
    users.check_csrf_token(request.form['csrf_token'])
    contact_id = request.form['contact_id']
    users.cancel_contact_request(int(contact_id))
    alias = request.form['alias']
    toast_text = f'Contact request to {alias} cancelled.'
    return render_template('users.html', toastText=toast_text)


@app.route('/answer_contact_request', methods=['POST'])
def answer_contact_request():
    users.check_csrf_token(request.form['csrf_token'])
    alias = request.form['alias']
    toast_text = None
    if 'accept' in request.form:
        users.accept_request(request.form['accept'])
        toast_text = f'Contact request by {alias} accepted.'
    if 'decline' in request.form:
        users.decline_request(request.form['decline'])
        toast_text = f'Contact request by {alias} declined.'
    return render_template('users.html', toastText=toast_text)


@app.route('/set_list_filter', methods=['POST'])
def set_list_filter():
    users.check_csrf_token(request.form['csrf_token'])
    users.set_list_filter(request.form['list_filter'])
    return redirect('/users')


@app.route('/create_new_token', methods=['POST'])
def create_new_token():
    users.check_csrf_token(request.form['csrf_token'])
    users.create_new_token()
    toast_text = f'Contact token created.'
    return render_template('profile.html', toastText=toast_text)


@app.route('/delete_contact_token', methods=['POST'])
def delete_contact_token():
    users.check_csrf_token(request.form['csrf_token'])
    users.delete_contact_token(request.form['token_id'])
    toast_text = f'Contact token deleted.'
    return render_template('profile.html', toastText=toast_text)


@app.route('/change_profile_visibility', methods=['POST'])
def change_profile_visibility():
    users.check_csrf_token(request.form['csrf_token'])
    if request.form['visibility'] == 'true':
        users.change_profile_visibility(request.form['visibility'])
        toast_text = f'Profile made visible.'
    else:
        users.change_profile_visibility(request.form['visibility'])
        toast_text = f'Profile hidden.'
    return render_template('profile.html', toastText=toast_text)


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
