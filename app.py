from flask import Flask
from flask import redirect, render_template, request, session
from os import getenv, path
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import secrets

basedir = path.abspath(path.dirname(__file__))
env_dir = path.join(basedir, '.env')
load_dotenv(env_dir)

print(basedir)
print(env_dir)
#print(getenv("SECRET_KEY"))

app = Flask(__name__)
app.secret_key = getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')

#print('SECRET_KEY:', app.secret_key)
#print('DATABASE_URL:', app.config['SQLALCHEMY_DATABASE_URI'])

db = SQLAlchemy(app)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#session["test"] = "aybabtu"


@app.route('/')
def index():
    contacts = []
    threads = []
    if 'username' in session:
        contacts = ['Annika', 'Kempesteri', 'Noora', 'Emmi']
        threads = ['Thread 1', 'Thread 2', 'Thread 3']
    return render_template('index.html', contacts=contacts, threads=threads)


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    sql = text('SELECT id, username, password, alias, visibility FROM users WHERE username=:username')
    result = db.session.execute(sql, {'username': username})
    user = result.fetchone()
    print(user)
    if user[2] == password:
        session['username'] = user[1]
        session['alias'] = user[3]
        session['visibility'] = user[4]

    return redirect('/')


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')


@app.route('/create_user')
def create_user():
    return render_template('create_user.html')
@app.route('/new_user', methods=['POST'])
def new_user():
    print(request.form)
    username = request.form['username']
    password = request.form['password']
    alias = request.form['alias']
    visibility = True if 'visibility' in request.form else False
    sql = text('SELECT id, username FROM users WHERE username=:username')
    result = db.session.execute(sql, {'username': username})
    user = result.fetchone()
    print(username, password, alias, visibility)

    if user:
        print('USER FOUND: ', user)
        return redirect('/create_user')
    else:
        sql = text('INSERT INTO users (username, password, alias, visibility) VALUES (:username, :password, :alias, :visibility)')
        db.session.execute(sql, {'username': username, 'password': password, 'alias': alias, 'visibility': visibility})
        db.session.commit()
    return redirect('/')


def get_token():
    token = secrets.token_hex(16)
    return token


if __name__ == '__main__':
    app.run()
