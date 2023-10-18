from flask import session, abort
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
        session['csrf_token'] = get_token()

        load_user_session()

        print('LOGIN')
        return True

    print('LOGIN FAILED')
    return False


def logout():
    if 'user_id' in session:
        del session['user_id']
    if 'username' in session:
        del session['username']
    if 'alias' in session:
        del session['alias']
    if 'visible' in session:
        del session['visible']
    if 'csrf_token' in session:
        del session['csrf_token']
    if 'users' in session:
        del session['users']
    if 'contact_requests' in session:
        del session['contact_requests']
    if 'contacts' in session:
        del session['contacts']
    if 'threads' in session:
        del session['threads']
    if 'messages' in session:
        del session['messages']
    if 'selected_thread_id' in session:
        del session['selected_thread_id']
    if 'selected_user' in session:
        del session['selected_user']

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

    login(username, password)

    return True


def delete_user():

    user_id = session['user_id']
    sql = text('SELECT id, username FROM users WHERE id=:id')
    result = db.session.execute(sql, {'id': user_id})
    user = result.fetchone()

    if user:
        sql = text('DELETE FROM users WHERE id=:id')
        db.session.execute(sql, {'id': user_id})
        return True

    logout()

    return False


def delete_contact(contact_id):

    print('HEP!')
    print(contact_id)

    sql = text('DELETE FROM ONLY contacts WHERE (user_id=:user_id AND contact_id=:contact_id) OR (user_id=:contact_id AND contact_id=:user_id)')
    db.session.execute(sql, {'user_id': session['user_id'], 'contact_id': contact_id})
    db.session.commit()

    get_contacts()

    return


def load_user_session():
    get_users()
    get_contact_requests()
    get_contacts()
    correspondence.get_threads()
    return


def get_users():

    sql = text('SELECT id, alias FROM users WHERE visible=:visible AND NOT id=:id')
    result = db.session.execute(sql, {'visible': True, 'id': session['user_id']})
    users = result.fetchall()

    status = check_if_contact(users)

    ret = []
    for user in users:
        u = {'id': user[0], 'alias': user[1], 'status': status[user[0]]}
        ret.append(u)

    session['users'] = ret

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

    session['contact_requests'] = ret

    return ret


def check_if_contact(user_list, ind=0):
    ret = {}

    for i in user_list:
        sql = text('SELECT id, pending FROM contacts WHERE (user_id=:user_id AND contact_id=:contact_id) OR (user_id=:contact_id AND contact_id=:user_id)')
        result = db.session.execute(sql, {'user_id': session['user_id'], 'contact_id': i[ind]})
        contact = result.fetchone()
        if contact:
            if contact[1]:
                ret[i[ind]] = 'pending'
            else:
                ret[i[ind]] = 'contact'
        else:
            ret[i[ind]] = 'none'

    return ret

def get_contacts():

    sql = text('SELECT id, alias FROM users WHERE id = ANY(SELECT contact_id FROM contacts WHERE user_id=:id AND pending=:pending UNION SELECT user_id FROM contacts WHERE contact_id=:id AND pending=:pending)')
    result = db.session.execute(sql, {'id': session['user_id'], 'pending': False})
    users = result.fetchall()

    status = check_if_contact(users)

    ret = []
    for user in users:
        u = {'id': user[0], 'alias': user[1], 'status': status[user[0]]}
        ret.append(u)

    session['contacts'] = ret

    return ret


def select_user(contact_id):

    sql = text('SELECT id, alias FROM users WHERE id=:id')
    result = db.session.execute(sql, {'id': contact_id})
    user = result.fetchone()

    # sql = text('SELECT id FROM contacts WHERE (user_id=:user_id AND contact_id=:contact_id) OR (user_id=:contact_id AND contact_id=:user_id)')
    # result = db.session.execute(sql, {'user_id': session['user_id'], 'contact_id': contact_id})
    # contact = result.fetchone()
    #
    # print(contact)
    #
    # is_contact = False
    # if contact:
    #     is_contact = True

    # is_contact = True if check_if_contact([user]) else False

    ret = {'id': user[0], 'alias': user[1], 'status': check_if_contact([user])[user[0]]}
    print(ret)
    session['selected_user'] = ret

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

    get_users()

    return True


def cancel_contact_request(contact_id):
    print('DEL', contact_id)
    sql = text('DELETE FROM ONLY contacts WHERE user_id=:user_id AND contact_id=:contact_id AND pending=:pending')
    db.session.execute(sql, {'user_id': session['user_id'], 'contact_id': contact_id, 'pending': True})
    db.session.commit()
    get_users()
    return


def send_request_by_token(request_token):

    sql = text('SELECT id, user_id FROM contact_tokens WHERE token=:token AND active=:active')
    result = db.session.execute(sql, {'token': request_token, 'active': True})
    user = result.fetchone()

    get_users()

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

    get_users()
    get_contact_requests()

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

    get_contact_requests()

    return True


def get_token(num=12):
    token = secrets.token_hex(num)
    return token


def check_csrf_token(token):
    if token == session['csrf_token']:
        return True
    else:
        abort(403)


#print(get_token())
