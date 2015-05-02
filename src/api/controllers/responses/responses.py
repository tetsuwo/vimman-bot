# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, session, request
from helpers.crossdomain import *
from models.model import *

from datetime import datetime as dt
from config.databases import *
import json

import logging
LOG_FILENAME = 'example.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

app = Blueprint(__name__, "responses")

@app.route('/', methods=['POST'])
@crossdomain(origin='*')
def create():
    if request.headers['Content-Type'] != 'application/json':
        return jsonify(message='error'), 400
    tdatetime = dt.now()
    created_at = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    # 下記 三項演算子で記述する
    creator_by = 0 # TODO: created user
    req = json.loads(request.data)
    try:
        response = Response(
            id=None,
            type=req["type"],
            content=req["content"],
            state=req["state"],
            created_by=creator_by,
            updated_by=creator_by,
            created_at=created_at,
            updated_at=created_at
        )
        db_session.add(response)
	db_session.flush()
        db_session.commit()
	result = {}
	result['id'] = response.id
	result['type'] = response.type
	result['content'] = response.content
	result['state'] = response.state
    	return jsonify(result=result), 201
    except:
	logging.error(req)
    return '', 400

@app.route('/', methods=['GET'])
@crossdomain(origin='*')
def index():
    code = 200
    try:
    	responses = []
    	res = Response.query.all()
    	for row in res:
            responses.append(row)
        responses_dict = ListResponseMapper({'result': responses}).as_dict()
        result = responses_dict['result']
        return jsonify(result=result), 200
    except:
	logging.error(request)
    return '', 404

@app.route('/<response_id>', methods=['GET'])
@crossdomain(origin='*')
def read(response_id):
    try:
    	response = (
		Response.query
		.filter("id = :response_id")
		.params(response_id=response_id)
		.first()
	)
        response_dict = ResponseMapper(response).as_dict()
    	return jsonify(result=response_dict), 200
    except:
	logging.error(request)
    return '', 404

@app.route('/<response_id>', methods=['PUT'])
#@app.route('/<response_id>', methods=['POST'])
@crossdomain(origin='*')
def update(response_id):
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    req = request.form

    # 下記 三項演算子で記述する
    updater_id = 0
    if session.get('user_id') is not None:
        updater_id = session.get('user_id')

    try:
        row = db_session.query(Response).get(response_id)
        row.type = req["responses[type]"]
        row.content = req["responses[content]"]
        row.state = req["responses[state]"]
        row.updated_by = updater_id
        row.updated_at = tstr

        db_session.flush()
        db_session.commit()
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
        db_session.commit()
    except:
        pass
    finally:
        pass

    return jsonify(status_code=code)
