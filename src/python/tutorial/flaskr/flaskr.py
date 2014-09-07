# -*- coding: utf-8 -*-

import sqlite3
from flask import Flask, jsonify, Response, request, session, g, redirect, url_for, abort, render_template, flash

import json
from functools import wraps
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

users = {
  1: {'id':1, 'name':'foo'},
  2: {'id':2, 'name':'bar'}
}

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

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')

    app.logger.debug(users.values())
    #content_body_dict = json.loads(request.form)
    #content_body_dict['id'] = 1000
    #response = jsonify(content_body_dict)
    app.logger.debug(request.data)
    app.logger.debug(request.form.values())
    app.logger.debug(jsonify(users.values()))
    #app.logger.debug(json.dumps({'tets':'dddd'}))

    return redirect(url_for('show_entries'))
@app.route('/test')
def test():
  return jsonify(result=users.values())

@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

#@app.route('/apitest/create')
  
if __name__ == '__main__':
  app.run()
