# -*- coding: utf-8 -*-
import sqlite3
from flask import Flask, jsonify, Response, request, session, g, redirect, url_for, abort, render_template, flash
from datetime import datetime as dt

DATABASE = 'vim_man.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTING', silent=True)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

from contextlib import closing
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def test():
    res = {1: 2}
    return jsonify(res)

# /operations

@app.route('/operations', methods=['POST'])
def add_operation():
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    # TODO saltのセット方法
    g.db.execute('insert into operations (username, password, salt, state, created_at, updated_at) values (?,?,?,?,?,?)',
            [request.form['username'], request.form['password'], "salt1", request.form['state'], tstr, tstr])
    g.db.commit()

    return jsonify(status_code=code)

@app.route('/operations', methods=['GET'])
def index_operatinos():
    code = 200
    # TODO passwordを外す
    cur = g.db.execute('select id, username, password, state, created_at, updated_at from operations')
    operations = [dict(id=row[0], username=row[1], password=row[2], state=row[3], created_at=row[4], updated_at=row[5]) for row in cur.fetchall()]
    # app.logger.debug(questions)
    return jsonify(status_code=code, result=operations)

@app.route('/operations/<operation_id>', methods=['GET'])
def show_operation(operation_id):
    code = 200
    cur = g.db.execute('select id, username, password, state, created_at, updated_at from operations where id = ?',
            [operation_id])
    operation = [dict(id=row[0], username=row[1], password=row[2], state=row[3], created_at=row[4], updated_at=row[5]) for row in cur.fetchall()]

    return jsonify(status_code=code, result=operation)

@app.route('/operations/<operation_id>', methods=['PUT'])
def edit_operation(operation_id):
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    cur = g.db.execute('update operations set username=?, password=?, state=?, updated_at=? where id = ?',
            [request.form['username'], request.form['password'], request.form['state'], tstr, operation_id])
    g.db.commit()

    return jsonify(status_code=code)

@app.route('/operations/<operation_id>', methods=['DELETE'])
def delete_operation(operation_id):
    code = 204
    cur = g.db.execute('delete from operations where id = ?',
    [operation_id])
    g.db.commit()

    return jsonify(status_code=code)

# /questions
@app.route('/questions', methods=['GET'])
def index_questions():
    code = 200
    cur = g.db.execute('select id, content, state, created_by, updated_by, created_at, updated_at from questions')
    questions = [dict(id=row[0], content=row[1], state=row[2], created_by=row[3], updated_by=row[4], created_at=row[5], updated_at=row[6]) for row in cur.fetchall()]
    # app.logger.debug(questions)
    return jsonify(status_code=code, result=questions)

@app.route('/questions', methods=['POST'])
def add_question():
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    g.db.execute('insert into questions (content, state, created_by, updated_by, created_at, updated_at) values (?,?,?,?,?,?)',
            [request.form['content'], request.form['state'], request.form['created_by'], request.form['updated_by'], tstr, tstr])
    g.db.commit()

    return jsonify(status_code=code)

@app.route('/questions/<question_id>', methods=['GET'])
def show_question(question_id):
    code = 200
    cur = g.db.execute('select id, content, state, created_by, updated_by, created_at, updated_at from questions where id = ?',
            [question_id])
    question = [dict(id=row[0], content=row[1], state=row[2], created_by=row[3], updated_by=row[4], created_at=row[5], updated_at=row[6]) for row in cur.fetchall()]

    return jsonify(status_code=code, result=question)

@app.route('/questions/<question_id>', methods=['PUT'])
def edit_question(question_id):
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    app.logger.debug(request.form)
    cur = g.db.execute('update questions set content=?, state=?, updated_by=?, updated_at=? where id = ?',
            [request.form['content'], request.form['state'], request.form['updated_by'], tstr, question_id])
    g.db.commit()

    return jsonify(status_code=code)

@app.route('/questions/<question_id>', methods=['DELETE'])
def delete_question(question_id):
    code = 204
    cur = g.db.execute('delete from questions where id = ?',
    [question_id])
    g.db.commit()

    return jsonify(status_code=code)


# /answers
@app.route('/answers/<question_id>', methods=['POST'])
def add_answer(question_id):
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    g.db.execute('insert into answers (question_id, content, state, created_by, updated_by, created_at, updated_at) values (?,?,?,?,?,?,?)',
            [question_id, request.form['content'], request.form['state'], request.form['created_by'], request.form['updated_by'], tstr, tstr])
    g.db.commit()

    return jsonify(status_code=code)

@app.route('/answers/<question_id>', methods=['GET'])
def index_answers(question_id):
    code = 200
    cur = g.db.execute('select id, question_id, content, state, created_by, updated_by, created_at, updated_at from answers where question_id = ?',
            question_id)
    answers = [dict(id=row[0], question_id=row[1], content=row[2], state=row[3], created_by=row[4], updated_by=row[5], created_at=row[6], updated_at=row[7]) for row in cur.fetchall()]

    return jsonify(status_code=code, result=answers)

@app.route('/answers/<question_id>/<answer_id>', methods=['GET'])
def show_answer(question_id, answer_id):
    code = 200
    cur = g.db.execute('select id, question_id, content, state, created_by, updated_by, created_at, updated_at from answers where id = ?',
            [answer_id])
    question = [dict(id=row[0], question_id=row[1], content=row[2], state=row[3], created_by=row[4], updated_by=row[5], created_at=row[6], updated_at=row[7]) for row in cur.fetchall()]

    return jsonify(status_code=code, result=question)

@app.route('/answers/<question_id>/<answer_id>', methods=['PUT'])
def edit_answer(question_id, answer_id):
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    cur = g.db.execute('update answers set content=?, state=?, updated_by=?, updated_at=? where id = ?',
            [request.form['content'], request.form['state'], request.form['updated_by'], tstr, answer_id])
    g.db.commit()

    return jsonify(status_code=code)

@app.route('/answers/<question_id>/<answer_id>', methods=['DELETE'])
def delete_answer(question_id, answer_id):
    code = 204
    cur = g.db.execute('delete from answers where question_id = ? and id = ?',
    [question_id, answer_id])
    g.db.commit()

    return jsonify(status_code=code)

# /informations
@app.route('/informations', methods=['POST'])
def add_information():
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    g.db.execute('insert into informations (content, state, created_by, updated_by, created_at, updated_at) values (?,?,?,?,?,?)',
            [request.form['content'], request.form['state'], request.form['created_by'], request.form['updated_by'], tstr, tstr])
    g.db.commit()

    return jsonify(status_code=code)

@app.route('/informations', methods=['GET'])
def index_informations():
    code = 200
    cur = g.db.execute('select id, content, state, created_by, updated_by, created_at, updated_at from informations')
    informations = [dict(id=row[0], content=row[1], state=row[2], created_by=row[3], updated_by=row[4], created_at=row[5], updated_at=row[6]) for row in cur.fetchall()]
    # app.logger.debug(questions)
    return jsonify(status_code=code, result=informations)

@app.route('/informations/<information_id>', methods=['GET'])
def show_information(information_id):
    code = 200
    cur = g.db.execute('select id, content, state, created_by, updated_by, created_at, updated_at from informations where id = ?',
            [information_id])
    information = [dict(id=row[0], content=row[1], state=row[2], created_by=row[3], updated_by=row[4], created_at=row[5], updated_at=row[6]) for row in cur.fetchall()]

    return jsonify(status_code=code, result=information)

@app.route('/informations/<information_id>', methods=['PUT'])
def edit_information(information_id):
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    cur = g.db.execute('update informations set content=?, state=?, updated_by=?, updated_at=? where id = ?',
            [request.form['content'], request.form['state'], request.form['updated_by'], tstr, information_id])
    g.db.commit()

    return jsonify(status_code=code)

@app.route('/informations/<information_id>', methods=['DELETE'])
def delete_information(information_id):
    code = 204
    cur = g.db.execute('delete from informations where id = ?',
    [information_id])
    g.db.commit()

    return jsonify(status_code=code)

# /tweets
@app.route('/tweets', methods=['GET'])
def index_tweets():
    # create dummy data
    #g.db.execute('insert into tweets (tweet_id, type, content, created_by, updated_by, created_at, updated_at) values (1,"ok","rers","himejima","update_himejima","2013/11/11 11:11:32", "2014/12/11 10:50:22")')
    #g.db.commit()

    code = 200
    cur = g.db.execute('select id, tweet_id, type, content, created_by, updated_by, created_at, updated_at from tweets')
    tweets = [dict(id=row[0], tweet_id=row[1], type=row[2], created_by=row[3], updated_by=row[4], created_at=row[5], updated_at=row[6]) for row in cur.fetchall()]
    # app.logger.debug(questions)
    return jsonify(status_code=code, result=tweets)

# /responses
@app.route('/responses', methods=['POST'])
def add_response():
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    g.db.execute('insert into responses (type, content, state, created_by, updated_by, created_at, updated_at) values (?,?,?,?,?,?,?)',
            [request.form['type'], request.form['content'], request.form['state'], request.form['created_by'], request.form['updated_by'], tstr, tstr])
    g.db.commit()

    return jsonify(status_code=code)

@app.route('/responses', methods=['GET'])
def index_responses():
    code = 200
    cur = g.db.execute('select id, type, content, state, created_by, updated_by, created_at, updated_at from responses')
    responses = [dict(id=row[0], type=row[1], content=row[2], state=row[3], created_by=row[4], updated_by=row[5], created_at=row[6], updated_at=row[7]) for row in cur.fetchall()]
    # app.logger.debug(questions)
    return jsonify(status_code=code, result=responses)

@app.route('/responses/<response_id>', methods=['GET'])
def show_response(response_id):
    code = 200
    cur = g.db.execute('select id, type, content, state, created_by, updated_by, created_at, updated_at from responses where id = ?',
            [response_id])
    response = [dict(id=row[0], type=row[1], content=row[2], state=row[3], created_by=row[4], updated_by=row[5], created_at=row[6], updated_at=row[7]) for row in cur.fetchall()]

    return jsonify(status_code=code, result=response)

@app.route('/responses/<response_id>', methods=['PUT'])
def edit_response(response_id):
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    cur = g.db.execute('update responses set type=?, content=?, state=?, updated_by=?, updated_at=? where id = ?',
            [request.form['type'], request.form['content'], request.form['state'], request.form['updated_by'], tstr, response_id])
    g.db.commit()

    return jsonify(status_code=code)

@app.route('/responses/<response_id>', methods=['DELETE'])
def delete_response(response_id):
    code = 204
    cur = g.db.execute('delete from responses where id = ?',
    [response_id])
    g.db.commit()

    return jsonify(status_code=code)

# /login
@app.route('/login', methods=['GET', 'POST'])
def login():
    code = 200
    error = None
    if request.method == 'POST':
        if request.form['username'] == app.config['USERNAME'] and request.form['password'] == app.config['PASSWORD']:
            session['logged_in'] = True
            return jsonify(status_code=code)
        else:
            error = 'wrong' 

    return jsonify(status_code=code)

# /logout
@app.route('/logout')
def logout():
    code = 200
    session.pop('logged_in', None)
    return jsonify(status_code=code)

if __name__ == '__main__':
    app.run()
