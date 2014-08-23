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

# /questions
@app.route('/questions', methods=['GET'])
def index_questions():
    cur = g.db.execute('select id, content, created_by, updated_by, created_at, updated_at from questions')
    questions = [dict(id=row[0], content=row[1], created_by=row[2], updated_by=row[3], created_at=row[4], updated_at=row[5]) for row in cur.fetchall()]
    app.logger.debug(questions)
    return jsonify(result=questions)

@app.route('/questions', methods=['POST'])
def add_question():
    #g.db.execute('insert into questions (content, created_by, updated_by, created_at, updated_at) values (?,?,?,?,?)',[])
    g.db.execute('insert into questions (content, state, created_by, updated_by, created_at, updated_at) values (?,?,?,?,?,?)',
            [request.form['content'], request.form['state'], request.form['created_by'], request.form['updated_by'], request.form['created_at'], request.form['updated_at']])
    g.db.commit()
    #app.logger.debug(request.data)
    app.logger.debug(request.form['content'])
    app.logger.debug(request.form['state'])
    app.logger.debug(request.form['created_by'])
    app.logger.debug(request.form['updated_by'])
    app.logger.debug(request.form['state'])
    app.logger.debug(request.form['created_at'])
    app.logger.debug(request.form['updated_at'])
    return jsonify({0:3})

@app.route('/questions/<question_id>', methods=['GET'])
def show_question(question_id):
    cur = g.db.execute('select id, content, created_by, updated_by, created_at, updated_at from questions where id = 1')
    question = [dict(id=row[0], content=row[1], created_by=row[2], updated_by=row[3], created_at=row[4], updated_at=row[5]) for row in cur.fetchall()]
    #response.result = jsonify(question)
    #response.status_code = 200
    return jsonify(result=question)

@app.route('/questions/<question_id>', methods=['PUT'])
def edit_question(question_id):
    #app.logger.debug(request.form)
    cur = g.db.execute('update questions set content="update_con", state=1 where id = 1')
    g.db.commit()
    return jsonify({"request_method": "put"})

@app.route('/questions/<question_id>', methods=['DELETE'])
def delete_question(question_id):
    cur = g.db.execute('delete from questions where id = ?',
    [question_id])
    g.db.commit()
    return jsonify({0:"deleteです"})


# /answers

# /informations

# /tweets

# /responses

# /login

# /logout

if __name__ == '__main__':
    app.run()
