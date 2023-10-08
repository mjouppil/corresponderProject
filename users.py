from flask import redirect, render_template, request, session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
import secrets
from app import db
import correspondence

def login(username, password):

    sql = text('SELECT id, username, password, alias, visible FROM users WHERE username=:username')
    result = db.session.execute(sql, {'username': username})
    user = result.fetchone()

    if user and check_password_hash(user[2], password):
        session['user_id'] = user[0]
        session['username'] = user[1]
        session['alias'] = user[3]
        session['visible'] = user[4]

        load_user_session()

        print('LOGIN')
        return True

    return False


def logout():
    del session['user_id']
    del session['username']
    del session['alias']
    del session['visible']
    del session['users']
    del session['contact_requests']
    del session['contacts']
    del session['threads']

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


def load_user_session():
    session['users'] = get_users()
    session['contact_requests'] = get_contact_requests()
    session['contacts'] = get_contacts()
    session['threads'] = correspondence.get_threads()
    return


def get_users():

    sql = text('SELECT id, alias FROM users WHERE visible=:visible AND NOT id=:id')
    result = db.session.execute(sql, {'visible': True, 'id': session['user_id']})
    users = result.fetchall()

    ret = []
    for user in users:
        u = {'id': user[0], 'alias': user[1]}
        ret.append(u)

    return ret


def get_contact_requests():

    sql = text('SELECT id, alias FROM users WHERE id = ANY(SELECT user_id FROM contacts WHERE contact_id=:id AND pending=:pending)')
    result = db.session.execute(sql, {'id': session['user_id'], 'pending': True})
    users = result.fetchall()

    print('Request users', users)

    ret = []
    for user in users:
        u = {'id': user[0], 'alias': user[1]}
        ret.append(u)
    print('request_ret', ret)

    return ret


def get_contacts():

    sql = text('SELECT id, alias FROM users WHERE id = ANY(SELECT contact_id FROM contacts WHERE user_id=:id AND pending=:pending UNION SELECT user_id FROM contacts WHERE contact_id=:id AND pending=:pending)')
    result = db.session.execute(sql, {'id': session['user_id'], 'pending': False})
    users = result.fetchall()

    ret = []
    for user in users:
        u = {'id': user[0], 'alias': user[1]}
        ret.append(u)

    return ret


def send_request(contact_id):

    user_id = session['user_id']

    sql = text('SELECT id, username FROM users WHERE id=:id')
    result = db.session.execute(sql, {'id': contact_id})
    user = result.fetchone()

    if not user:
        print('USER NOT FOUND')
        return False

    sql = text('INSERT INTO contacts (user_id, contact_id, pending) VALUES (:user_id, :contact_id, :pending)')
    db.session.execute(sql, {'user_id': user_id, 'contact_id': contact_id, 'pending': True})
    db.session.commit()

    return True


def send_request_by_token(request_token):

    sql = text('SELECT id, user_id FROM contact_tokens WHERE token=:token AND active=:active')
    result = db.session.execute(sql, {'token': request_token, 'active': True})
    user = result.fetchone()

    return


def accept_request(id):

    sql = text('SELECT id, user_id, contact_id, pending FROM contacts WHERE user_id=:id AND contact_id=:contact_id')
    result = db.session.execute(sql, {'id': id, 'contact_id': session['user_id']})
    contact = result.fetchone()

    if not contact:
        print('CONTACT NOT FOUND: ', contact)
        return False

    sql = text('UPDATE contacts SET pending = False WHERE user_id=:id AND contact_id=:contact_id')
    db.session.execute(sql, {'id': id, 'contact_id': session['user_id']})
    db.session.commit()

    return True


def decline_request(id):

    sql = text('SELECT id, user_id, contact_id, pending FROM contacts WHERE user_id=:id AND contact_id=:contact_id')
    result = db.session.execute(sql, {'id': id, 'contact_id': session['user_id']})
    contact = result.fetchone()

    if not contact:
        print('CONTACT NOT FOUND: ', contact)
        return False

    sql = text('DELETE FROM contacts WHERE user_id=:id AND contact_id=:contact_id')
    db.session.execute(sql, {'id': id, 'contact_id': session['user_id']})
    db.session.commit()

    return True


def get_token(num: 12):
    token = secrets.token_hex(num)
    return token

#print(get_token())
