# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request, session
from helpers.crossdomain import *
from models.model import *

from datetime import datetime as dt
from config.databases import *
import json

import logging
LOG_FILENAME = 'example.log'
logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %p %I:%M:%S'
)

app = Blueprint(__name__, 'questions')

@app.route('/', methods=['POST'])
@crossdomain(origin='*')
def create():
    if request.headers['Content-Type'] != 'application/json':
        return jsonify(message='error'), 400
    tdatetime = dt.now()
    created_at = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    created_by = 0 # TODO: created user
    req = json.loads(request.data)
    try:
        db_session.begin()
        question = Question(
            id=None,
            content=req['content'].encode('utf-8'),
            state=req['state'],
            created_by=created_by,
            updated_by=created_by,
            created_at=created_at,
            updated_at=created_at
        )
        db_session.add(question)
        db_session.flush()
        answers = req['answers'].split('\r\n')
        logging.error(answers)
        for answer_text in answers:
            answer = Answer(
                id=None,
                question_id=question.id,
                content=answer_text,
                state=1,
                created_by=created_by,
                updated_by=created_by,
                created_at=created_at,
                updated_at=created_at
            )
            db_session.add(answer)
        db_session.flush()
        db_session.commit()
        result = {}
        result['id'] = question.id
        result['state'] = question.state
        result['content'] = question.content
        return jsonify(result=result), 201
    except:
        logging.error(req)
        db_session.rollback()
    return '', 400

@app.route('/', methods=['GET'])
@crossdomain(origin='*')
def index_questions():
    """質問一覧を返却します
    """
    code = 200
    #logging.debug(request.headers)
    # TODO 公開時にコメントイン
    #if request.headers['Api-Key'] != API_ACCESS_KEY:
    #    abort(401)

    questions_dict = {}
    try:
        questions = get_questions()
        #logging.debug(questions)
        questions_dict = ListQuestionMapper({'result': questions}).as_dict()
    except:
        pass
    logging.debug(questions_dict)
    result = questions_dict['result']

    return jsonify(status_code=code, result=result)

@app.route('/<question_id>', methods=['GET'])
@crossdomain(origin='*')
def show_question(question_id):
    """idを元に質問データを取得します
    """
    code = 200
    question_dict = {}

    try:
        question = get_question(question_id)
        question_dict = QuestionMapper(question).as_dict()
    except:
        # 取得に失敗
        pass

    return jsonify(status_code=code, result=question_dict)

def get_question(question_id):
    """質問idを元にQuestionモデルを返却する
    """
    #logging.debug(Question.query.first().id)
    question = []
    question = Question.query.filter("id = :question_id").params(question_id=question_id).first()

    return question

def get_questions():
    """質問一覧のリストを返却する
    """
    questions = []
    res = Question.query.all()
    for row in res:
        questions.append(row)

    return questions

@app.route('/<question_id>', methods=['PUT'])
@crossdomain(origin='*')
def edit_question(question_id):
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    req = request.form

    # 下記 三項演算子で記述する
    updater_id = 0
    if session.get('user_id') is not None:
        updater_id = session.get('user_id')

    try:
        # Question
        row = db_session.query(Question).get(question_id)
        row.content = req["questions[content]"]
        row.state = req["questions[state]"]
        row.updated_by = updater_id
        row.updated_at = tstr

        # Answer delete -> insert
        answers = req['questions[answer]'].split('\r\n')
        # answerもdeleteする
        row_a = Answer.query.filter(Answer.question_id == question_id).all()
        for row in row_a:
            db_session.delete(row)

        db_session.flush()
        db_session.commit()

        for row in answers:
            answer = Answer(
                    id = None,
                    question_id=question_id,
                    content=row,
                    state=1,
                    created_by=updater_id,
                    updated_by=updater_id,
                    created_at=tstr,
                    updated_at=tstr
            )
            db_session.add(answer)

        db_session.commit()

    except:
        pass
    finally:
        pass

    return jsonify(status_code=code)

@app.route('/<question_id>', methods=['DELETE'])
@crossdomain(origin='*')
def delete_question(question_id):
    code = 204
    try:
        # answerもdeleteする
        row_a = Answer.query.filter(Answer.question_id == question_id).all()
        #logging.debug(row_a)
        #db_session.delete(row_a)
        for row in row_a:
            db_session.delete(row)


        row = Question.query.get(question_id)
        db_session.delete(row)

        db_session.flush()
        db_session.commit()
    except:
        pass
    finally:
        pass

    return jsonify(status_code=code)


