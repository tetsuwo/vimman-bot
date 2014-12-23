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

from models.model import *

@app.before_request
def before_request():
    pass

@app.teardown_request
def teardown_request(exception):
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

from users import users
app.register_blueprint(users.app, url_prefix="/users")
#@app.route('/')
#@crossdomain(origin='*')
#def test():
#    res = {1: 2}
#    return jsonify(res)

if __name__ == '__main__':
    app.run()
