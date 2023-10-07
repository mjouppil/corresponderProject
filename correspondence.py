from flask import redirect, render_template, request, session
from sqlalchemy.sql import text
import datetime
from app import db


def new_thread(name):
    user_id = session['user_id']
    print(user_id)

    sql = text('INSERT INTO threads (name) VALUES (:name) RETURNING id')
    res1 = db.session.execute(sql, {'name': name})
    res2 = db.session.commit()

    print(res1)
    print(res2)

    sql = text('INSERT INTO user_threads (user_id, thread_id) VALUES (:user_id, :thread_id) RETURNING id')
    res3 = db.session.execute(sql, {'user_id': user_id, 'thread_id': thread_id})
    res4 = db.session.commit()

    print(res3)
    print(res4)

    return


def new_message(thread_id, message):
    user_id = session['user_id']
    print(user_id)

    time = datetime.datetime.now()

    sql = text('INSERT INTO messages (user_id, thread_id, message, time) VALUES (:user_id, :thread_id, :message, :time) RETURNING id')
    res1 = db.session.execute(sql, {'user_id': user_id, 'thread_id':thread_id, 'message':message, 'time':time})
    res2 = db.session.commit()
    print(res1)
    print(res2)

    return


def get_threads():
    user_id = session['user_id']
    print(user_id)

    sql = text('SELECT id, name FROM threads WHERE thread_id IN (SELECT thread_id FROM user_threads WHERE userd_id=:user_id)')
    result = db.session.execute(sql, {'user_id': user_id})
    threads = result.fetchall()
    print(threads)

    return threads


def get_messages(thread_id):
    sql = text('SELECT id, message, time FROM messages WHERE thread_id=:thread_id ORDER BY time')
    result = db.session.execute(sql, {'thread_id': thread_id})
    messages = result.fetchall()
    print(messages)

    return messages
