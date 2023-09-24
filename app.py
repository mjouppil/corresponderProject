from flask import Flask
from flask import redirect, render_template, request, session
from os import getenv, path
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import secrets

basedir = path.abspath(path.dirname(__file__))
env_dir = path.join(basedir, 'venv', '.env')
load_dotenv(env_dir)

#print(basedir)
#print(env_dir)
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
    session['username'] = username
    return redirect('/')


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')


def get_token():
    token = secrets.token_hex(16)
    return token


if __name__ == '__main__':
    app.run()
