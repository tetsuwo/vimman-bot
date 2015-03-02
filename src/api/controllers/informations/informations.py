# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request, session
from helpers.crossdomain import *
from models.model import *

from datetime import datetime as dt
from config.databases import *
import json

import logging
LOG_FILENAME = 'example.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

app = Blueprint(__name__, "informations")

@app.route('/', methods=['POST'])
@crossdomain(origin='*')
def create():
    if request.headers['Content-Type'] != 'application/json':
        print(request.headers['Content-Type'])
        return jsonify(message='error'), 400
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    req = json.loads(request.data)
    result = {}
    created_by = 0 # TODO: created user
    try:
        information = Information(
            id=None,
            content=req['content'].encode('utf-8'),
            state=req['state'],
            created_by=created_by,
            updated_by=created_by,
            created_at=tstr,
            updated_at=tstr
        )
        db_session.add(information)
        db_session.flush()
        db_session.commit()
        result['id'] = information.id
        result['state'] = information.state
        result['content'] = information.content
    except:
        logging.error(req)
        return '', 404
        pass
    finally:
        pass

    return jsonify(result=result), 201

#@app.route('/', methods=['GET'])
#@crossdomain(origin='*')
#def read():
#    """お知らせの一覧を取得します
#    """
#    code = 200
#    informations_dict = {}
#
#    try:
#        informations = get_informations()
#        informations_dict = ListInformationMapper({'result': informations}).as_dict()
#    except:
#        pass
#
#    logging.debug(informations_dict)
#    result = informations_dict['result']
#
#    return jsonify(status_code=code, result=result)

@app.route('/<information_id>', methods=['GET'])
@crossdomain(origin='*')
def readone(information_id):
    information_dict = {}
    try:
        information = get_information(information_id)
        information_dict = InformationMapper(information).as_dict()
    except:
        return '', 404
        pass
    return jsonify(result=information_dict), 200

def get_information(information_id):
    information = None
    information = Information.query.filter("id = :information_id").params(information_id=information_id).first()
    return information

#def get_informations():
#    informations = []
#    res = Information.query.all()
#    for row in res:
#        informations.append(row)
#
#    return informations

@app.route('/<information_id>', methods=['PUT'])
@crossdomain(origin='*')
def update(information_id):
    if request.headers['Content-Type'] != 'application/json':
        print(request.headers['Content-Type'])
        return jsonify(message='error'), 400
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    req = json.loads(request.data)
    result = {}
    updated_by = 0
    try:
        row = db_session.query(Information).get(information_id)
        row.content = req['content']
        row.state = req['state']
        row.updated_by = updated_by
        row.updated_at = tstr
        db_session.flush()
        db_session.commit()
        result['id'] = row.id
        result['state'] = row.state
        result['content'] = row.content
    except:
        logging.error(req)
        return '', 404
        pass
    finally:
        pass
    return jsonify(result=result), 201

@app.route('/<information_id>', methods=['DELETE'])
@crossdomain(origin='*')
def delete(information_id):
    try:
        row = Information.query.get(information_id)
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
