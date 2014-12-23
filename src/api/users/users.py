# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify
from helpers.crossdomain import *
from models.model import *

import logging
LOG_FILENAME = 'example.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

app = Blueprint(__name__, "users")

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

@app.route('/logout', methods=['GET'])
@crossdomain(origin='*')
def logout():
    """ ログアウトします
    """
    code = 200
    clear_session()
    return redirect('/#/login')
    #return jsonify(status_code=code)

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


def clear_session():
    session.clear()
