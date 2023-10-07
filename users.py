from flask import redirect, render_template, request, session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
import secrets
from app import db


def login(username, password):

    sql = text('SELECT id, username, password, alias, visible FROM users WHERE username=:username')
    result = db.session.execute(sql, {'username': username})
    user = result.fetchone()

    # check_password_hash(user[2], password)
    # user[2] == password

    if user and check_password_hash(user[2], password):
        session['user_id'] = user[0]
        session['username'] = user[1]
        session['alias'] = user[3]
        session['visible'] = user[4]
        print('LOGIN')
        return True

    return False


def logout():
    del session['user_id']
    del session['username']
    del session['alias']
    del session['visible']
    print('LOGOUT')
    return True


def register(request):

    username = request.form['username']
    password = request.form['password']
    alias = request.form['alias']
    visible = True if 'visible' in request.form else False
    print(username, password, alias, visible)

    sql = text('SELECT id, username FROM users WHERE username=:username')
    result = db.session.execute(sql, {'username': username})
    user = result.fetchone()

    if user:
        print('USER FOUND: ', user)
        return False

    hashed_password = generate_password_hash(password)

    sql = text('INSERT INTO users (username, password, alias, visible) VALUES (:username, :password, :alias, :visible)')
    db.session.execute(sql, {'username': username, 'password': hashed_password, 'alias': alias, 'visible': visible})
    db.session.commit()

    return True


def delete():

    user_id = session['user_id']
    sql = text('SELECT id, username FROM users WHERE id=:id')
    result = db.session.execute(sql, {'id': user_id})
    user = result.fetchone()

    if user:
        sql = text('DELETE FROM users WHERE id=:id')
        db.session.execute(sql, {'id': user_id})
        return True

    return False


def get_users():

    sql = text('SELECT id, alias FROM users WHERE visible=:visible AND NOT id=:id')
    result = db.session.execute(sql, {'visible': True, 'id': session['user_id']})
    users = result.fetchall()
    print(users)
    session['userlist'] = users

    return


def get_contacts():

    sql = text('SELECT id, alias FROM users WHERE user_id IN (SELECT contact_id AS c_id FROM contacts WHERE user_id:id UNION SELECT user_id AS c_id FROM contacts WHERE contact_id:id)')
    result = db.session.execute(sql, {'id': session['user_id''']})
    contacts = result.fetchall()
    print(contacts)
    session['contacts'] = contacts

    return


def send_request(contact_id):

    user_id = session['user_id']

    sql = text('SELECT id, username FROM users WHERE username=:username')
    result = db.session.execute(sql, {'username': username})
    user = result.fetchone()

    if user:
        print('USER FOUND: ', user)
        return False

    sql = text('INSERT INTO contacts (user_id, contact_id, pending) VALUES (:user_id :contact_id, :pending)')
    db.session.execute(sql, {'user_id': user_id, 'contact_id': contact_id, 'pending': True})
    db.session.commit()

    return True


def send_request_by_token(request_token):

    sql = text('SELECT id, user_id FROM contact_tokens WHERE token=:token AND active=:active')
    result = db.session.execute(sql, {'token': request_token, 'active': True})
    user = result.fetchone()

    return


def accept_request(contacts_id):

    sql = text('SELECT id, user_id, contact_id, pending FROM contacts WHERE id=:contacts_id')
    result = db.session.execute(sql, {'contacts_id': contacts_id})
    contact = result.fetchone()

    if not contact:
        print('CONTACT NOT FOUND: ', contact)
        return False

    sql = text('UPDATE contacts SET pending = False WHERE id=:contacts_id')
    db.session.execute(sql, {'contacts_id': contacts_id})
    db.session.commit()

    return True


def reject_request(contacts_id):

    sql = text('SELECT id, user_id, contact_id, pending FROM contacts WHERE id=:contacts_id')
    result = db.session.execute(sql, {'contacts_id': contacts_id})
    contact = result.fetchone()

    if not contact:
        print('CONTACT NOT FOUND: ', contact)
        return False

    sql = text('DELETE FROM contacts WHERE id=:contacts_id')
    db.session.execute(sql, {'contacts_id': contacts_id})
    db.session.commit()

    return True


def get_token(num: 12):
    token = secrets.token_hex(num)
    return token

#print(get_token())
