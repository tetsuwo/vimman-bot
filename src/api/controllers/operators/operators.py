# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request, _request_ctx_stack
from helpers.crossdomain import *
from models.model import *

from datetime import datetime as dt
from config.databases import *

import logging
LOG_FILENAME = 'example.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

app = Blueprint(__name__, "operators")

@app.before_request
def before_request():
    method = request.form.get('_method', '').upper()
    logging.debug(method)
    if method:
        request.environ['REQUEST_METHOD'] = method
        ctx = _request_ctx_stack.top
        ctx.url_adapter.default_method = method
        assert request.method == method

@app.route('/', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def add_operator():
    """ 管理者を追加します
    """
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    req = request.form
    #logging.debug(req)
    # TODO saltのセット方法 + パスワードを暗号化する
    try:
        operator = Operator(
            id=None,
            username=req['operators[username]'],
            password=req['operators[password]'],
            salt='salt1',
            state=req['operators[state]'],
            created_at=tstr,
            updated_at=tstr
        )
        #operator = Operator(
        #    id=None,
        #    username=req['username'],
        #    password=req['password'],
        #    salt='salt1',
        #    state=req['state'],
        #    created_at=tstr,
        #    updated_at=tstr
        #)
        db_session.add(operator)
        db_session.commit()
    except:
        # 登録失敗
        pass
    finally:
        pass

    return jsonify(status_code=code)

@app.route('/', methods=['GET'])
@crossdomain(origin='*')
def index_operators():
    code = 200
    try:
        operators = get_operators()
        operators_dict = ListOperatorMapper({'result': operators}).as_dict()
    except:
        pass

    result = operators_dict['result']

    return jsonify(status_code=code, result=result)

@app.route('/<operator_id>', methods=['GET'])
@crossdomain(origin='*')
def show_operator(operator_id):
    code = 200
    operator_dict = {}
    try:
        operator = get_operator(operator_id)
        operator_dict = OperatorMapper(operator).as_dict()
    except:
        # 取得に失敗
        pass
    
    return jsonify(status_code=code, result=operator_dict)

def get_operator(operator_id):
    operator = None
    operator = Operator.query.filter("id = :operator_id").params(operator_id=operator_id).first()

    return operator

def get_operators():
    operators = []
    res = Operator.query.all()
    for row in res:
        operators.append(row)

    return operators

#TODO PUTリクエストする方法を考える
#@app.route('/operators/<operator_id>', methods=['PUT'])
#@app.route('/<operator_id>', methods=['PUT'])
@app.route('/<operator_id>', methods=['POST'])
@crossdomain(origin='*')
def edit_operator(operator_id):
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    req = request.form
    try:
        row = db_session.query(Operator).get(operator_id)
        row.username = req['operators[username]']
        row.password = req['operators[password]']
        row.state = req['operators[state]']
        row.updated_at = tstr
        db_session.flush()
        # なぜ必要？ 調査
        db_session.commit()
    except:
        pass
    finally:
        pass

    return jsonify(status_code=code)

@app.route('/<operator_id>', methods=['DELETE'])
@crossdomain(origin='*')
def delete_operator(operator_id):
    """ 管理者を削除します
    """
    code = 204
    try:
        row = Operator.query.get(operator_id)
        db_session.delete(row)
        db_session.flush()
    except:
        pass
    finally:
        pass

    return jsonify(status_code=code)
