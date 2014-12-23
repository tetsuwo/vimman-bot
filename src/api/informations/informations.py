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

@app.route('/', methods=['GET'])
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

@app.route('/<information_id>', methods=['GET'])
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

@app.route('/<information_id>', methods=['PUT'])
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

@app.route('/<information_id>', methods=['DELETE'])
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
