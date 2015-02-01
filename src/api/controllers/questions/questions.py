# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request, session
from helpers.crossdomain import *
from models.model import *

from datetime import datetime as dt

import logging
LOG_FILENAME = 'example.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

app = Blueprint(__name__, "questions")

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

# TODO answerも同時に登録するように修正すること
@app.route('/', methods=['POST'])
@crossdomain(origin='*')
def add_question():
    """リクエストを元に質問を登録します
    """
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    req = request.form
    creator_id = session.get('user_id')
    #logging.debug(req['content'])
    #logging.debug(req['state'])
    #logging.debug(req['created_by'])
    #logging.debug(req['updated_by'])
    #try:
    # question
    question = Question(
        id=None,
        content=req['questions[content]'],
        state=req['questions[state]'],
        created_by=creator_id,
        updated_by=creator_id,
        created_at=tstr,
        updated_at=tstr
    )
    db_session.add(question)
    db_session.commit()

    # req['questions[answer]']を分解する
    answers = req['questions[answer]'].split('\r\n')
    for row in answers:
        #TODO 空だったら continueする
        # answer
        answer = Answer(
            id=None,
            question_id=question.id,
            content=row,
            state=1,
            created_by=creator_id,
            updated_by=creator_id,
            created_at=tstr,
            updated_at=tstr
        )
        db_session.add(answer)
 
    db_session.commit()
    #except:
    #    # 登録失敗
    #    db_session.rollback()
    #finally:
    #    db_session.close()

    return jsonify(status_code=code)

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

