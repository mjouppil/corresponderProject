from flask import session
from sqlalchemy.sql import text
import datetime
from app import db


def new_thread(name, contacts):
    sql = text('INSERT INTO threads (name) VALUES (:name) RETURNING id')
    result = db.session.execute(sql, {'name': name})
    db.session.commit()
    thread_id = result.fetchone()[0]

    participants = [int(i) for i in contacts]
    participants.append(session['user_id'])

    sql = text('INSERT INTO user_threads (user_id, thread_id) VALUES (unnest(:participants), :thread_id) RETURNING id')
    result = db.session.execute(sql, {'participants': participants, 'thread_id': thread_id})
    db.session.commit()
    result.fetchone()

    get_threads()
    select_thread(thread_id)
    get_messages()

    return True


def new_message(message):
    time = datetime.datetime.now()
    sql = text('INSERT INTO messages (user_id, thread_id, message, time) VALUES (:user_id, :thread_id, :message, :time) RETURNING id')
    db.session.execute(sql, {'user_id': session['user_id'], 'thread_id': session['selected_thread_id'], 'message': message, 'time': time})
    db.session.commit()

    get_messages()
    return


def get_threads():
    sql = text('SELECT id, name FROM threads WHERE id IN (SELECT thread_id FROM user_threads WHERE user_id=:user_id)')
    result = db.session.execute(sql, {'user_id': session['user_id']})
    threads = result.fetchall()

    ret = []
    for thread in threads:
        t = {'id': thread[0], 'name': thread[1]}
        ret.append(t)

    session['threads'] = ret
    return ret


def get_messages():
    sql = text('SELECT messages.id, message, time, users.id, users.alias FROM messages INNER JOIN users ON users.id = messages.user_id WHERE thread_id=:thread_id ORDER BY time')
    result = db.session.execute(sql, {'thread_id': session['selected_thread_id']})
    messages = result.fetchall()

    ret = []
    for message in messages:
        m = {'id': message[0], 'message': message[1], 'time': message[2], 'user_id': message[3], 'user_alias': message[4]}
        ret.append(m)

    print(ret)
    session['messages'] = ret
    return


def select_thread(thread_id):
    session['selected_thread_id'] = thread_id
    get_messages()
    return
