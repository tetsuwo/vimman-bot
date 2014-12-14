# -*- coding: utf-8 -*-

from flask import Flask, jsonify, Response, request, \
     session, g, redirect, url_for, abort, render_template, flash
from datetime import datetime as dt
from helpers.crossdomain import *
from helpers.database import *
from config.databases import *
import MySQLdb

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTING', silent=True)

@app.before_request
def before_request():
    g.connection = MySQLdb.connect(
        host=db_config["host"],
        db=db_config["db"],
        user=db_config["user"],
        passwd=db_config["passwd"],
        port=db_config["port"],
        unix_socket=db_config["unix_socket"]
    )
    g.cursor = g.connection.cursor()

@app.teardown_request
def teardown_request(exception):
    cursor = getattr(g, 'cursor', None)
    if cursor is not None:
        cursor.close()

    connection = getattr(g, 'connection', None)
    if connection is not None:
        connection.close()

@app.route('/')
@crossdomain(origin='*')
def test():
    res = {1: 2}
    print session
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return '''
        <form action="/login" method="post">
            <p><input type=text name=username></p>
            <p><input type=password name=password></p>
            <p><input type=submit value=Login></p>
        </form>
    '''
    #return jsonify(res)

# /operations

@app.route('/operations', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def add_operation():
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    # TODO saltのセット方法
    g.cursor.execute('insert into operations (username, password, salt, state, created_at, updated_at) values (%s,%s,%s,%s,%s,%s)',
            ([request.form['username'], request.form['password'], "salt1", request.form['state'], tstr, tstr]))
    g.connection.commit()

    return jsonify(status_code=code)

@app.route('/operations', methods=['GET'])
@crossdomain(origin='*')
def index_operatinos():
    code = 200
    # TODO passwordを外す
    # cur = g.db.execute('select id, username, password, state, created_at, updated_at from operations')
    g.cursor.execute('select id, username, password, state, created_at, updated_at from operations')
    operations = g.cursor.fetchall()

    # print operations
    #operations = [dict(id=row[0], username=row[1], password=row[2], state=row[3], created_at=row[4], updated_at=row[5]) for row in g.cursor.fetchall()]
    operations = [dict(id=row[0], username=row[1], password=row[2], state=row[3], created_at=row[4], updated_at=row[5]) for row in operations]
    # app.logger.debug(questions)
    # operations = 200
    return jsonify(status_code=code, result=operations)

@app.route('/operations/<operation_id>', methods=['GET'])
@crossdomain(origin='*')
def show_operation(operation_id):
    code = 200
    g.cursor.execute('select id, username, password, state, created_at, updated_at from operations where id = %s',
            [operation_id])
    operation = [dict(id=row[0], username=row[1], password=row[2], state=row[3], created_at=row[4], updated_at=row[5]) for row in g.cursor.fetchall()]

    return jsonify(status_code=code, result=operation)

@app.route('/operations/<operation_id>', methods=['PUT'])
@crossdomain(origin='*')
def edit_operation(operation_id):
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    g.cursor.execute('update operations set username = %s, password = %s, state = %s, updated_at = %s where id = %s',
            ([request.form['username'], request.form['password'], request.form['state'], tstr, operation_id]))
    g.connection.commit()

    return jsonify(status_code=code)

@app.route('/operations/<operation_id>', methods=['DELETE'])
@crossdomain(origin='*')
def delete_operation(operation_id):
    code = 204
    g.cursor.execute('delete from operations where id = %s',
    ([operation_id]))
    g.connection.commit()

    return jsonify(status_code=code)

# /questions
@app.route('/questions', methods=['GET'])
@crossdomain(origin='*')
def index_questions():
    code = 200
    g.cursor.execute('select id, content, state, created_by, updated_by, created_at, updated_at from questions')
    questions = [dict(id=row[0], content=row[1], state=row[2], created_by=row[3], updated_by=row[4], created_at=row[5], updated_at=row[6]) for row in g.cursor.fetchall()]
    # app.logger.debug(questions)
    return jsonify(status_code=code, result=questions)

@app.route('/questions', methods=['POST'])
@crossdomain(origin='*')
def add_question():
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    g.cursor.execute('insert into questions (content, state, created_by, updated_by, created_at, updated_at) values (%s, %s, %s, %s, %s, %s)',
            ([request.form['content'], request.form['state'], request.form['created_by'], request.form['updated_by'], tstr, tstr]))
    g.connection.commit()

    return jsonify(status_code=code)

@app.route('/questions/<question_id>', methods=['GET'])
@crossdomain(origin='*')
def show_question(question_id):
    code = 200
    g.cursor.execute('select id, content, state, created_by, updated_by, created_at, updated_at from questions where id = %s',
            ([question_id]))
    question = [dict(id=row[0], content=row[1], state=row[2], created_by=row[3], updated_by=row[4], created_at=row[5], updated_at=row[6]) for row in g.cursor.fetchall()]

    return jsonify(status_code=code, result=question)

@app.route('/questions/<question_id>', methods=['PUT'])
@crossdomain(origin='*')
def edit_question(question_id):
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    # app.logger.debug(request.form)
    g.cursor.execute('update questions set content = %s, state = %s, updated_by = %s, updated_at = %s where id = %s',
            ([request.form['content'], request.form['state'], request.form['updated_by'], tstr, question_id]))
    g.connection.commit()

    return jsonify(status_code=code)

@app.route('/questions/<question_id>', methods=['DELETE'])
@crossdomain(origin='*')
def delete_question(question_id):
    code = 204
    g.cursor.execute('delete from questions where id = %s',
    [question_id])
    g.connection.commit()

    return jsonify(status_code=code)


# /answers
@app.route('/answers/<question_id>', methods=['POST'])
@crossdomain(origin='*')
def add_answer(question_id):
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    g.cursor.execute('insert into answers (question_id, content, state, created_by, updated_by, created_at, updated_at) values (%s, %s, %s, %s, %s, %s, %s)',
            ([question_id, request.form['content'], request.form['state'], request.form['created_by'], request.form['updated_by'], tstr, tstr]))
    g.connection.commit()

    return jsonify(status_code=code)

@app.route('/questions/<question_id>/answers', methods=['GET'])
@crossdomain(origin='*')
def index_answers(question_id):
    code = 200
    g.cursor.execute('select id, question_id, content, state, created_by, updated_by, created_at, updated_at from answers where question_id = %s',
            question_id)
    answers = [dict(id=row[0], question_id=row[1], content=row[2], state=row[3], created_by=row[4], updated_by=row[5], created_at=row[6], updated_at=row[7]) for row in g.cursor.fetchall()]

    return jsonify(status_code=code, result=answers)

@app.route('/answers/<answer_id>', methods=['GET'])
@crossdomain(origin='*')
def show_answer(answer_id):
    code = 200
    g.cursor.execute('select id, question_id, content, state, created_by, updated_by, created_at, updated_at from answers where id = %s',
            [answer_id])
    question = [dict(id=row[0], question_id=row[1], content=row[2], state=row[3], created_by=row[4], updated_by=row[5], created_at=row[6], updated_at=row[7]) for row in g.cursor.fetchall()]

    return jsonify(status_code=code, result=question)

@app.route('/answers/<answer_id>', methods=['PUT'])
@crossdomain(origin='*')
def edit_answer(answer_id):
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    g.cursor.execute('update answers set content = %s, state = %s, updated_by = %s, updated_at = %s where id = %s',
            ([request.form['content'], request.form['state'], request.form['updated_by'], tstr, answer_id]))
    g.connection.commit()

    return jsonify(status_code=code)

@app.route('/answers/<answer_id>', methods=['DELETE'])
@crossdomain(origin='*')
def delete_answer(answer_id):
    code = 204
    g.cursor.execute('delete from answers where id = %s',
    [answer_id])
    g.connection.commit()

    return jsonify(status_code=code)

# /informations
@app.route('/informations', methods=['POST'])
@crossdomain(origin='*')
def add_information():
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    g.cursor.execute('insert into informations (content, state, created_by, updated_by, created_at, updated_at) values (%s, %s, %s, %s, %s, %s)',
            [request.form['content'], request.form['state'], request.form['created_by'], request.form['updated_by'], tstr, tstr])
    g.connection.commit()

    return jsonify(status_code=code)

@app.route('/informations', methods=['GET'])
@crossdomain(origin='*')
def index_informations():
    code = 200
    g.cursor.execute('select id, content, state, created_by, updated_by, created_at, updated_at from informations')
    informations = [dict(id=row[0], content=row[1], state=row[2], created_by=row[3], updated_by=row[4], created_at=row[5], updated_at=row[6]) for row in g.cursor.fetchall()]
    # app.logger.debug(questions)
    return jsonify(status_code=code, result=informations)

@app.route('/informations/<information_id>', methods=['GET'])
@crossdomain(origin='*')
def show_information(information_id):
    code = 200
    g.cursor.execute('select id, content, state, created_by, updated_by, created_at, updated_at from informations where id = %s',
            [information_id])
    information = [dict(id=row[0], content=row[1], state=row[2], created_by=row[3], updated_by=row[4], created_at=row[5], updated_at=row[6]) for row in g.cursor.fetchall()]

    return jsonify(status_code=code, result=information)

@app.route('/informations/<information_id>', methods=['PUT'])
@crossdomain(origin='*')
def edit_information(information_id):
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    g.cursor.execute('update informations set content = %s, state = %s, updated_by = %s, updated_at = %s where id = %s',
            ([request.form['content'], request.form['state'], request.form['updated_by'], tstr, information_id]))
    g.connection.commit()

    return jsonify(status_code=code)

@app.route('/informations/<information_id>', methods=['DELETE'])
@crossdomain(origin='*')
def delete_information(information_id):
    code = 204
    g.cursor.execute('delete from informations where id = %s',
    [information_id])
    g.connection.commit()

    return jsonify(status_code=code)

# /tweets
@app.route('/tweets', methods=['GET'])
@crossdomain(origin='*')
def index_tweets():
    # create dummy data
    #g.db.execute('insert into tweets (tweet_id, type, content, created_by, updated_by, created_at, updated_at) values (1,"ok","rers","himejima","update_himejima","2013/11/11 11:11:32", "2014/12/11 10:50:22")')
    #g.db.commit()

    code = 200
    g.cursor.execute('select id, tweet_id, type, content, created_by, updated_by, created_at, updated_at from tweets')
    tweets = [dict(id=row[0], tweet_id=row[1], type=row[2], created_by=row[3], updated_by=row[4], created_at=row[5], updated_at=row[6]) for row in g.cursor.fetchall()]
    # app.logger.debug(questions)
    return jsonify(status_code=code, result=tweets)

# /responses
@app.route('/responses', methods=['POST'])
@crossdomain(origin='*')
def add_response():
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    g.cursor.execute('insert into responses (type, content, state, created_by, updated_by, created_at, updated_at) values (%s, %s, %s, %s, %s, %s, %s)',
            ([request.form['type'], request.form['content'], request.form['state'], request.form['created_by'], request.form['updated_by'], tstr, tstr]))
    g.connection.commit()

    return jsonify(status_code=code)

@app.route('/responses', methods=['GET'])
@crossdomain(origin='*')
def index_responses():
    code = 200
    g.cursor.execute('select id, type, content, state, created_by, updated_by, created_at, updated_at from responses')
    responses = [dict(id=row[0], type=row[1], content=row[2], state=row[3], created_by=row[4], updated_by=row[5], created_at=row[6], updated_at=row[7]) for row in g.cursor.fetchall()]
    # app.logger.debug(questions)
    return jsonify(status_code=code, result=responses)

@app.route('/responses/<response_id>', methods=['GET'])
@crossdomain(origin='*')
def show_response(response_id):
    code = 200
    g.cursor.execute('select id, type, content, state, created_by, updated_by, created_at, updated_at from responses where id = %s',
            [response_id])
    response = [dict(id=row[0], type=row[1], content=row[2], state=row[3], created_by=row[4], updated_by=row[5], created_at=row[6], updated_at=row[7]) for row in g.cursor.fetchall()]

    return jsonify(status_code=code, result=response)

@app.route('/responses/<response_id>', methods=['PUT'])
@crossdomain(origin='*')
def edit_response(response_id):
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    g.cursor.execute('update responses set type = %s, content = %s, state = %s, updated_by = %s, updated_at = %s where id = %s',
            ([request.form['type'], request.form['content'], request.form['state'], request.form['updated_by'], tstr, response_id]))
    g.connection.commit()

    return jsonify(status_code=code)

@app.route('/responses/<response_id>', methods=['DELETE'])
@crossdomain(origin='*')
def delete_response(response_id):
    code = 204
    g.cursor.execute('delete from responses where id = %s',
    [response_id])
    g.connection.commit()

    return jsonify(status_code=code)

# /login
@app.route('/login', methods=['GET', 'POST'])
@crossdomain(origin='*')
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
@crossdomain(origin='*')
def logout():
    code = 200
    session.pop('logged_in', None)
    return jsonify(status_code=code)

if __name__ == '__main__':
    app.run()
