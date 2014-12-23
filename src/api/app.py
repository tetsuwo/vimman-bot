# -*- coding: utf-8 -*-

from flask import Flask, jsonify, Response, request, \
     session, g, redirect, url_for, abort, render_template, flash
from datetime import datetime as dt
from helpers.crossdomain import *
from helpers.database import *
from config.databases import *

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
import MySQLdb
import logging
#import json
from bpmappers import Mapper, RawField, DelegateField, ListDelegateField

API_ACCESS_KEY = 'himejimaspecial'
LOG_FILENAME = 'example.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = 'my secret key'

app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTING', silent=True)

# create base
engine = create_engine("mysql://root:@localhost:3306/vimmanbot",echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

from models.model import *

@app.before_request
def before_request():
    pass

@app.teardown_request
def teardown_request(exception):
    pass

def clear_session():
    session.clear()
    pass

from questions import questions
app.register_blueprint(questions.app, url_prefix="/questions")

from operations import operations
app.register_blueprint(operations.app, url_prefix="/operations")

from informations import informations
app.register_blueprint(informations.app, url_prefix="/informations")

from responses import responses
app.register_blueprint(responses.app, url_prefix="/responses")

from tweets import tweets
app.register_blueprint(tweets.app, url_prefix="/tweets")

#@app.route('/')
#@crossdomain(origin='*')
#def test():
#    res = {1: 2}
#    return jsonify(res)



@app.route('/login', methods=['GET', 'POST'])
@crossdomain(origin='*')
def login():
    """ ログインします
    """
    code = 200
    error = None
    #logging.debug(request.form)

    if request.method == 'POST':
        #if request.form['username'] == app.config['USERNAME'] and request.form['password'] == app.config['PASSWORD']:
        if request.form['username'] == 'test' and request.form['password'] == 'pass':
            #session['logged_in'] = True
            set_username(request.form['username'])
            return redirect('/#/questions')
            #return jsonify(status_code=code)
        else:
            error = 'wrong'
            return redirect('/#/login')
            #return jsonify(error=error)

    return jsonify(status_code=code)

def set_username(username):
    session['username'] = username

def get_username():
    return session.get('username')

def is_login():
    return not not get_username()

def user_check():
    #logging.debug(is_login())
    if not is_login():
        logging.debug(is_login())
        abort(401)
        #return redirect('/#/login')

@app.route('/logout', methods=['GET'])
@crossdomain(origin='*')
def logout():
    """ ログアウトします
    """
    code = 200
    clear_session()
    return redirect('/#/login')
    #return jsonify(status_code=code)

if __name__ == '__main__':
    app.run()
