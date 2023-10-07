# from flask import Flask
# from flask import redirect, render_template, request, session
# from flask_bootstrap import Bootstrap
# from os import getenv, path
# from dotenv import load_dotenv
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.sql import text
# import secrets
#
# import routes
#
#
# def create_app():
#     basedir = path.abspath(path.dirname(__file__))
#     env_dir = path.join(basedir, '.env')
#     load_dotenv(env_dir)
#
#     c_app = Flask(__name__)
#     c_app.secret_key = getenv('SECRET_KEY')
#     c_app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
#     c_db = SQLAlchemy(c_app)
#     c_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     Bootstrap(c_app)
#
#     return c_app, c_db
#
#
# app, db = create_app()
#
#
# @app.route('/')
# def index():
#     contacts = []
#     threads = []
#     if 'username' in session:
#         contacts = ['Annika', 'Kempesteri', 'Noora', 'Emmi']
#         threads = ['Thread 1', 'Thread 2', 'Thread 3']
#     return render_template('index.html', contacts=contacts, threads=threads)
#
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'GET':
#         render_template('index.html')
#
#     username = request.form['username']
#     password = request.form['password']
#
#     sql = text('SELECT id, username, password, alias, visible FROM users WHERE username=:username')
#     result = db.session.execute(sql, {'username': username})
#     user = result.fetchone()
#
#     if user and user[2] == password:
#         session['user_id'] = user[0]
#         session['username'] = user[1]
#         session['alias'] = user[3]
#         session['visible'] = user[4]
#
#     return redirect('/')
#
#
# @app.route('/logout')
# def logout():
#     del session['username']
#     return redirect('/')
#
#
# @app.route('/create_user')
# def create_user():
#     return render_template('register.html')
#
#
# @app.route('/new_user', methods=['POST'])
# def new_user():
#
#     test_conn()
#
#     print(request.form)
#     username = request.form['username']
#     password = request.form['password']
#     alias = request.form['alias']
#     visible = 'true' if 'visible' in request.form else 'false'
#     sql = text('SELECT id, username FROM users WHERE username=:username')
#     result = db.session.execute(sql, {'username': username})
#     user = result.fetchone()
#     print(username, password, alias, visible)
#
#     if user:
#         print('USER FOUND: ', user)
#         return redirect('/create_user')
#     else:
#         sql = text('INSERT INTO users (username, password, alias, visible) VALUES (:username, :password, :alias, :visible)')
#         db.session.execute(sql, {'username': username, 'password': password, 'alias': alias, 'visible': visible})
#         db.session.commit()
#     return redirect('/')
#
#
# @app.route('/testA')
# def testA():
#     return render_template('base.html')
#
#
# def test_conn():
#     with app.app_context():
#         try:
#             # db.session.execute('SELECT 1')
#             db.session.execute(text('SELECT 1'))
#             print('\n\n----------- Connection successful !')
#         except Exception as e:
#             print('\n\n----------- Connection failed ! ERROR : ', e)
#     return
#
#
# if __name__ == '__main__':
#    app.run()
