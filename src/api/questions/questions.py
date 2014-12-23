# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify
from helpers.crossdomain import *
from models.model import *

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
    #logging.debug(req['content'])
    #logging.debug(req['state'])
    #logging.debug(req['created_by'])
    #logging.debug(req['updated_by'])
    try:
        question = Question(
                            id=None,
                            content=req['content'],
                            state=req['state'],
                            created_by=req['created_by'],
                            updated_by=req['updated_by'],
                            created_at=tstr,
                            updated_at=tstr
        )
        db_session.add(question)
        db_session.commit()
    except:
        # 登録失敗
        db_session.rollback()
    finally:
        db_session.close()

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

