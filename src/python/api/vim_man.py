# -*- coding: utf-8 -*-
import sqlite3
from flask import Flask, jsonify, Response, request, session, g, redirect, url_for, abort, render_template, flash

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
    pass

@app.route('/operations', methods=['GET'])
def index_operatinos():
    code = 200
    pass

@app.route('/operations/<operation_id>', methods=['GET'])
def show_operation(operation_id):
    code = 200
    pass

@app.route('/operations/<operation_id>', methods=['PUT'])
def edit_operation(operation_id):
    code = 201
    pass

@app.route('/operations/<operation_id>', methods=['DELETE'])
def delete_operation(operation_id):
    code = 204
    pass


# /questions
@app.route('/questions', methods=['GET'])
def index_questions():
    code = 200
    cur = g.db.execute('select id, content,state, created_by, updated_by, created_at, updated_at from questions')
    questions = [dict(id=row[0], content=row[1], state=row[2], created_by=row[3], updated_by=row[4], created_at=row[5], updated_at=row[6]) for row in cur.fetchall()]
    # app.logger.debug(questions)
    return jsonify(status_code=code, result=questions)

@app.route('/questions', methods=['POST'])
def add_question():
    code = 201
    #g.db.execute('insert into questions (content, created_by, updated_by, created_at, updated_at) values (?,?,?,?,?)',[])
    g.db.execute('insert into questions (content, state, created_by, updated_by, created_at, updated_at) values (?,?,?,?,?,?)',
            [request.form['content'], request.form['state'], request.form['created_by'], request.form['updated_by'], request.form['created_at'], request.form['updated_at']])
    g.db.commit()

    return jsonify(status_code=code)

@app.route('/questions/<question_id>', methods=['GET'])
def show_question(question_id):
    code = 200
    cur = g.db.execute('select id, content, created_by, updated_by, created_at, updated_at from questions where id = ?',
            [question_id])
    question = [dict(id=row[0], content=row[1], created_by=row[2], updated_by=row[3], created_at=row[4], updated_at=row[5]) for row in cur.fetchall()]

    return jsonify(status_code=code, result=question)

@app.route('/questions/<question_id>', methods=['PUT'])
def edit_question(question_id):
    code = 201
    #app.logger.debug(request.form)
    cur = g.db.execute('update questions set content=?, state=?, created_by=?, updated_by=? where id = ?',
            [request.form['content'], request.form['state'], request.form['created_by'], request.form['updated_at'], question_id])
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
def add_answer():
    code = 201
    pass

@app.route('/answers/<question_id>', methods=['GET'])
def index_answers():
    code = 200
    pass

@app.route('/answers/<question_id>/<answer_id>', methods=['GET'])
def show_answer(answer_id):
    code = 200
    pass

@app.route('/answers/<question_id>/<answer_id>', methods=['PUT'])
def edit_answer(answer_id):
    code = 201
    pass

@app.route('/answers/<question_id>/<answer_id>', methods=['DELETE'])
def delete_answer(answer_id):
    code = 204
    pass


# /informations
@app.route('/informations', methods=['POST'])
def add_information():
    code = 201
    pass

@app.route('/informations', methods=['GET'])
def index_informations():
    code = 200
    pass

@app.route('/informations/<information_id>', methods=['GET'])
def show_information(information_id):
    code = 200
    pass

@app.route('/informations/<information_id>', methods=['PUT'])
def edit_information(information_id):
    code = 201
    pass

@app.route('/informations/<information_id>', methods=['DELETE'])
def delete_information(information_id):
    code = 204
    pass

# /tweets
@app.route('/tweets', methods=['GET'])
def index_tweets():
    code = 200
    pass

# /responses
@app.route('/responses', methods=['POST'])
def add_response():
    code = 201
    pass

@app.route('/responses', methods=['GET'])
def index_responses():
    code = 200
    pass

@app.route('/responses/<response_id>', methods=['GET'])
def show_response(response_id):
    code = 200
    pass

@app.route('/responses/<response_id>', methods=['PUT'])
def edit_response(response_id):
    code = 201
    pass

@app.route('/responses/<response_id>', methods=['DELETE'])
def delete_response(response_id):
    code = 204
    pass

# /login

# /logout

if __name__ == '__main__':
    app.run()
