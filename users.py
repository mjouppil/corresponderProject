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
        return True

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
    if 'selected_user' in session:
        del session['list_filter']
    if 'contact_tokens' in session:
        del session['contact_tokens']
    return True


def register(request):

    username = request.form['username']
    password = request.form['password']
    alias = request.form['alias']
    visible = True if 'visible' in request.form else False

    sql = text('SELECT id, username FROM users WHERE username=:username')
    result = db.session.execute(sql, {'username': username})
    user = result.fetchone()

    if user:
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

    logout()
    return


def delete_contact(contact_id):
    sql = text('''DELETE FROM ONLY contacts WHERE
               (user_id=:user_id AND contact_id=:contact_id) OR (user_id=:contact_id AND contact_id=:user_id)''')
    db.session.execute(sql, {'user_id': session['user_id'], 'contact_id': contact_id})
    db.session.commit()

    get_users()
    return


def load_user_session():
    get_users()
    correspondence.get_threads()
    get_contact_tokens()
    session['list_filter'] = 'all'
    return


def get_users():
    contacts = get_contacts()
    requests = get_contact_requests()
    pending = get_pending_requests()

    ret = contacts.copy()
    ret.extend(requests)
    ret.extend(pending)

    sql = text('SELECT id, alias FROM users WHERE visible=:visible AND NOT id=:id')
    result = db.session.execute(sql, {'visible': True, 'id': session['user_id']})
    users = result.fetchall()

    ids = [i['id'] for i in ret]

    for user in users:
        u = {'id': user[0], 'alias': user[1], 'status': 'other'}
        if u['id'] not in ids:
            ret.append(u)

    session['users'] = ret
    return ret


def get_contact_requests():
    sql = text('''SELECT id, alias FROM users WHERE id = ANY(
               SELECT user_id FROM contacts WHERE contact_id=:id AND pending=:pending)''')
    result = db.session.execute(sql, {'id': session['user_id'], 'pending': True})
    users = result.fetchall()

    ret = []
    for user in users:
        u = {'id': user[0], 'alias': user[1], 'status': 'request'}
        ret.append(u)

    return ret


def get_pending_requests():
    sql = text('''SELECT id, alias FROM users WHERE id = ANY(
    SELECT contact_id FROM contacts WHERE user_id=:id AND pending=:pending) AND visible = :visible''')
    result = db.session.execute(sql, {'id': session['user_id'], 'pending': True, 'visible': True})
    users = result.fetchall()

    ret = []
    for user in users:
        u = {'id': user[0], 'alias': user[1], 'status': 'pending'}
        ret.append(u)

    return ret


def get_contacts():
    sql = text('''SELECT id, alias FROM users WHERE id = ANY(
    SELECT contact_id FROM contacts WHERE user_id=:id AND pending=:pending UNION 
    SELECT user_id FROM contacts WHERE contact_id=:id AND pending=:pending)''')
    result = db.session.execute(sql, {'id': session['user_id'], 'pending': False})
    users = result.fetchall()

    ret = []
    for user in users:
        u = {'id': user[0], 'alias': user[1], 'status': 'contact'}
        ret.append(u)

    session['contacts'] = ret
    return ret


def select_user(contact_id):
    ret = [i for i in session['users'] if int(i['id']) == int(contact_id)][0]
    session['selected_user'] = ret
    return ret


def send_request(contact_id):
    user_id = session['user_id']
    sql = text('SELECT id, username FROM users WHERE id=:id')
    result = db.session.execute(sql, {'id': contact_id})
    user = result.fetchone()

    if not user:
        return

    sql = text('INSERT INTO contacts (user_id, contact_id, pending) VALUES (:user_id, :contact_id, :pending)')
    db.session.execute(sql, {'user_id': user_id, 'contact_id': contact_id, 'pending': True})
    db.session.commit()

    get_users()
    return


def cancel_contact_request(contact_id):
    sql = text('DELETE FROM ONLY contacts WHERE user_id=:user_id AND contact_id=:contact_id AND pending=:pending')
    db.session.execute(sql, {'user_id': session['user_id'], 'contact_id': contact_id, 'pending': True})
    db.session.commit()

    get_users()
    return


def send_request_by_token(request_token):
    sql = text('SELECT user_id FROM contact_tokens WHERE token=:token AND active=:active')
    result = db.session.execute(sql, {'token': request_token, 'active': True})
    user = result.fetchone()

    if user:
        send_request(user[0])

    get_users()
    return


def accept_request(id):
    sql = text('SELECT id, user_id, contact_id, pending FROM contacts WHERE user_id=:id AND contact_id=:contact_id')
    result = db.session.execute(sql, {'id': id, 'contact_id': session['user_id']})
    result.fetchone()

    sql = text('UPDATE contacts SET pending = False WHERE user_id=:id AND contact_id=:contact_id')
    db.session.execute(sql, {'id': id, 'contact_id': session['user_id']})
    db.session.commit()

    get_users()
    return


def decline_request(id):
    sql = text('SELECT id, user_id, contact_id, pending FROM contacts WHERE user_id=:id AND contact_id=:contact_id')
    result = db.session.execute(sql, {'id': id, 'contact_id': session['user_id']})
    result.fetchone()

    sql = text('DELETE FROM contacts WHERE user_id=:id AND contact_id=:contact_id')
    db.session.execute(sql, {'id': id, 'contact_id': session['user_id']})
    db.session.commit()

    get_users()
    return


def set_list_filter(lf):
    session['list_filter'] = lf
    return


def create_new_token():
    sql = text('INSERT INTO contact_tokens (user_id, token, active) VALUES (:user_id, :token, :active)')
    db.session.execute(sql, {'user_id': session['user_id'], 'token': get_token(), 'active': True})
    db.session.commit()
    get_contact_tokens()
    return


def get_contact_tokens():
    sql = text('SELECT id, token, active FROM contact_tokens WHERE user_id=:user_id')
    result = db.session.execute(sql, {'user_id': session['user_id']})
    tokens = result.fetchall()

    ret = []
    for token in tokens:
        t = {'id': token[0], 'token': token[1], 'active': token[2]}
        ret.append(t)

    session['contact_tokens'] = ret
    return


def delete_contact_token(id):
    sql = text('DELETE FROM contact_tokens WHERE id=:id')
    db.session.execute(sql, {'id': id})
    db.session.commit()

    get_contact_tokens()
    return


def get_token(num=12):
    token = secrets.token_hex(num)
    return token


def change_profile_visibility(visibility):
    sql = text('UPDATE users SET visible=:visible WHERE id=:user_id')
    db.session.execute(sql, {'user_id': session['user_id'], 'visible': visibility})
    db.session.commit()

    refresh_user_session()
    return


def refresh_user_session():
    sql = text('SELECT id, username, alias, visible FROM users WHERE id=:user_id')
    result = db.session.execute(sql, {'user_id': session['user_id']})
    user = result.fetchone()

    session['user_id'] = user[0]
    session['username'] = user[1]
    session['alias'] = user[2]
    session['visible'] = user[3]
    return


def check_csrf_token(token):
    if token == session['csrf_token']:
        return True
    else:
        abort(403)
