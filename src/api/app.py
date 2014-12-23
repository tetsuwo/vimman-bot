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

#from informations import informations
#app.register_blueprint(informations.app, url_prefix="/informations")
#
#from responses import responses
#app.register_blueprint(responses.app, url_prefix="/responses")
#
from tweets import tweets
app.register_blueprint(tweets.app, url_prefix="/tweets")

#@app.route('/')
#@crossdomain(origin='*')
#def test():
#    res = {1: 2}
#    return jsonify(res)

@app.route('/informations', methods=['POST'])
@crossdomain(origin='*')
def add_information():
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    req = request.form
    # TODO SESSIONからloginユーザーをセットする
    creator = "creator"
    logging.debug(req['informations[content]'])

    try:
        information = Information(
                                  id=None,
                                  content=req['informations[content]'],
                                  state=req['informations[state]'],
                                  created_by=creator,
                                  updated_by=creator,
                                  created_at=tstr,
                                  updated_at=tstr
        )
        db_session.add(information)
        db_session.flush()
        db_session.commit()
    except:
        # 登録失敗
        pass
    finally:
        pass

    # TODO redirect処理を追加
    return jsonify(status_code=code)

@app.route('/informations', methods=['GET'])
@crossdomain(origin='*')
def index_informations():
    """お知らせの一覧を取得します
    """
    code = 200

    try:
        informations = get_informations()
        informations_dict = ListInformationMapper({'result': informations}).as_dict()
    except:
        pass

    result = informations_dict['result']

    return jsonify(status_code=code, result=result)

@app.route('/informations/<information_id>', methods=['GET'])
@crossdomain(origin='*')
def show_information(information_id):
    code = 200
    information_dict = {}

    try:
        information = get_information(information_id)
        information_dict = InformationMapper(information).as_dict()
    except:
        # 取得に失敗
        pass

    return jsonify(status_code=code, result=information_dict)

def get_information(information_id):
    information = []
    res = Information.query.filter("id = :information_id").params(information_id=information_id).first()
    information = Information(id=information_id,
                              content=res.content,
                              state=res.state,
                              created_by=res.created_by,
                              updated_by=res.updated_by,
                              created_at=res.created_at,
                              updated_at=res.updated_at
    )

    return information

def get_informations():
    informations = []
    res = Information.query.all()
    for row in res:
        informations.append(row)

    return informations

@app.route('/informations/<information_id>', methods=['PUT'])
@crossdomain(origin='*')
def edit_information(information_id):
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    req = request.form
    # TODO sessionから取得する
    updater = "updater"
    try:
        row = db_session.query(Information).get(information_id)
        row.content = req['informations[content]']
        row.state = req['informations[state]']
        row.updated_by = updater
        row.updated_at = tstr
        db_session.flush()
    except:
        pass
    finally:
        pass

    return jsonify(status_code=code)

@app.route('/informations/<information_id>', methods=['DELETE'])
@crossdomain(origin='*')
def delete_information(information_id):
    """お知らせを削除します
    """
    code = 204

    try:
        row = Information.query.get(information_id)
        db_session.delete(row)
        db_session.flush()
    except:
        pass
    finally:
        pass

    return jsonify(status_code=code)


@app.route('/responses', methods=['POST'])
@crossdomain(origin='*')
def add_response():
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    req = request.form
    creator = "creator111"

    try:
        response = Response(
                            id=None,
                            type=req["responses[type]"],
                            content=req["responses[content]"],
                            state=req["responses[state]"],
                            created_by=creator,
                            updated_by=creator,
                            created_at=tstr,
                            updated_at=tstr
        )
        db_session.add(response)
        db_session.commit()
    except:
        pass
    finally:
        pass

    return jsonify(status_code=code)

@app.route('/responses', methods=['GET'])
@crossdomain(origin='*')
def index_responses():
    code = 200
    try:
        responses = get_responses()
        responses_dict = ListResponseMapper({'result': responses}).as_dict()
    except:
        pass

    result = responses_dict['result']

    return jsonify(status_code=code, result=result)

@app.route('/responses/<response_id>', methods=['GET'])
@crossdomain(origin='*')
def show_response(response_id):
    code = 200
    response_dict = {}

    try:
        response = get_response(response_id)
        response_dict = ResponseMapper(response).as_dict()
    except:
        pass

    return jsonify(status_code=code, result=response_dict)

def get_response(response_id):
    response = []
    res = Response.query.filter("id = :response_id").params(response_id=response_id).first()
    response = Response(id=response_id,
                        type=res.type,
                        content=res.content,
                        state=res.state,
                        created_by=res.created_by,
                        updated_by=res.updated_by,
                        created_at=res.created_at,
                        updated_at=res.updated_at
    )

    return response

def get_responses():
    responses = []
    res = Response.query.all()
    for row in res:
        responses.append(row)

    return responses

@app.route('/responses/<response_id>', methods=['PUT'])
@crossdomain(origin='*')
def edit_response(response_id):
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    req = request.form
    updater = "updater"

    try:
        row = db_session.query(Response).get(response_id)
        row.type = req["responses[type]"]
        row.content = req["responses[content]"]
        row.state = req["responses[state]"]
        row.updated_by = updater
        row.updated_at = tstr

        db_session.flush()
    except:
        pass
    finally:
        pass

    return jsonify(status_code=code)

@app.route('/responses/<response_id>', methods=['DELETE'])
@crossdomain(origin='*')
def delete_response(response_id):
    code = 204
    try:
        row = Response.query.get(response_id)
        db_session.delete(row)
        db_session.flush()
    except:
        pass
    finally:
        pass

    return jsonify(status_code=code)

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
