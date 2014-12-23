# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify
from helpers.crossdomain import *
from models.model import *

import logging
LOG_FILENAME = 'example.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

app = Blueprint(__name__, "operations")

@app.route('/', methods=['POST'])
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

@app.route('/', methods=['GET'])
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

@app.route('/<response_id>', methods=['GET'])
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
    response = Response.query.filter("id = :response_id").params(response_id=response_id).first()

    return response

def get_responses():
    responses = []
    res = Response.query.all()
    for row in res:
        responses.append(row)

    return responses

@app.route('/<response_id>', methods=['PUT'])
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

@app.route('/<response_id>', methods=['DELETE'])
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
