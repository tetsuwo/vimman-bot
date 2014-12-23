# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify
from helpers.crossdomain import *
from models.model import *

import logging
LOG_FILENAME = 'example.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

app = Blueprint(__name__, "operations")

@app.route('/', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def add_operation():
    """ 管理者を追加します
    """
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    req = request.form
    # TODO saltのセット方法 + パスワードを暗号化する
    try:
        operation = Operation(
                              id=None,
                              username=req['operations[username]'],
                              password=req['operations[password]'],
                              salt='salt1',
                              state=req['operations[state]'],
                              created_at=tstr,
                              updated_at=tstr
        )
        db_session.add(operation)
        db_session.commit()
    except:
        # 登録失敗
        pass
    finally:
        pass

    return jsonify(status_code=code)

@app.route('/', methods=['GET'])
@crossdomain(origin='*')
def index_operatinos():
    code = 200
    try:
        operations = get_operations()
        operations_dict = ListOperationMapper({'result': operations}).as_dict()
    except:
        pass

    result = operations_dict['result']

    return jsonify(status_code=code, result=result)

@app.route('/<operation_id>', methods=['GET'])
@crossdomain(origin='*')
def show_operation(operation_id):
    code = 200
    operation_dict = {}
    try:
        operation = get_operation(operation_id)
        operation_dict = OperationMapper(operation).as_dict()
    except:
        # 取得に失敗
        pass
    
    return jsonify(status_code=code, result=operation_dict)

def get_operation(operation_id):
    operation = None
    operation = Operation.query.filter("id = :operation_id").params(operation_id=operation_id).first()

    return operation

def get_operations():
    operations = []
    res = Operation.query.all()
    for row in res:
        operations.append(row)

    return operations

#@app.route('/operations/<operation_id>', methods=['PUT'])
@app.route('/<operation_id>', methods=['PUT'])
@crossdomain(origin='*')
def edit_operation(operation_id):
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    req = request.form
    try:
        row = db_session.query(Operation).get(operation_id)
        row.username = req['operations[username]']
        row.password = req['operations[password]']
        row.state = req['operations[state]']
        row.updated_at = tstr
        db_session.flush()
    except:
        pass
    finally:
        pass

    return jsonify(status_code=code)

@app.route('/<operation_id>', methods=['DELETE'])
@crossdomain(origin='*')
def delete_operation(operation_id):
    """ 管理者を削除します
    """
    code = 204
    try:
        row = Operation.query.get(operation_id)
        db_session.delete(row)
        db_session.flush()
    except:
        pass
    finally:
        pass

    return jsonify(status_code=code)
