# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request, _request_ctx_stack
from helpers.crossdomain import *
from models.model import *

from datetime import datetime as dt
from config.databases import *
import json

import logging
LOG_FILENAME = 'example.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

app = Blueprint(__name__, 'operators')

@app.route('/', methods=['POST'])
@crossdomain(origin='*')
def add_operator():
    if request.headers['Content-Type'] != 'application/json':
        print(request.headers['Content-Type'])
        return jsonify(message='error'), 400
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    req = json.loads(request.data)
    result = {}
    try:
        # TODO: saltのセット方法 + パスワードを暗号化する
        operator = Operator(
            id=None,
            username=req['username'],
            password=req['password'],
            salt='salt1',
            state=req['state'],
            created_at=tstr,
            updated_at=tstr
        )
        db_session.add(operator)
        db_session.commit()
        result['id'] = operator.id
        result['username'] = operator.username
        result['state'] = operator.state
    except:
        logging.error(req)
        pass
    finally:
        pass

    return jsonify(result=result), 201

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
    operator_dict = {}
    try:
        operator = get_operator(operator_id)
        operator_dict = OperatorMapper(operator).as_dict()
    except:
        return '', 404
        pass

    return jsonify(result=operator_dict), 200

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

@app.route('/<operator_id>', methods=['PUT'])
@crossdomain(origin='*')
def edit_operator(operator_id):
    if request.headers['Content-Type'] != 'application/json':
        print(request.headers['Content-Type'])
        return jsonify(message='error'), 400
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    req = json.loads(request.data)
    result = {}
    try:
        row = db_session.query(Operator).get(operator_id)
        row.username = req['username']
        row.password = req['password']
        row.state = req['state']
        row.updated_at = tstr
        db_session.flush()
        # なぜ必要？ 調査
        db_session.commit()
        result['id'] = row.id
        result['username'] = row.username
        result['state'] = row.state
    except:
        logging.error(req)
        return '', 404
        pass
    finally:
        pass

    return jsonify(result=result), 201

@app.route('/<operator_id>', methods=['DELETE'])
@crossdomain(origin='*')
def delete_operator(operator_id):
    try:
        row = Operator.query.get(operator_id)
        db_session.delete(row)
        db_session.flush()
        db_session.commit()
    except:
        logging.error(request)
        return '', 404
        pass
    finally:
        pass

    return '', 204
