# -*- coding: utf-8 -*-

from flask import Flask, jsonify, Response, request, \
     session, g, redirect, url_for, abort, render_template, flash
from datetime import datetime as dt
from helpers.crossdomain import *
from helpers.database import *
from config.databases import *

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
import MySQLdb
import logging
#import json
from bpmappers import Mapper, RawField, DelegateField, ListDelegateField

API_ACCESS_KEY = 'himejimaspecial'
LOG_FILENAME = 'example.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = 'my secret key'

app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTING', silent=True)

# create base
engine = create_engine("mysql://root:@localhost:3306/vimmanbot",echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

from models.model import *

@app.before_request
def before_request():
    pass

@app.teardown_request
def teardown_request(exception):
    pass

# マッパークラス TODO 外に出すこと
## Mapper For Operation
class OperationMapper(Mapper):
    id = RawField()
    username = RawField()
    state = RawField()
    created_at = RawField()
    updated_at = RawField()

class ListOperationMapper(Mapper):
    result = ListDelegateField(OperationMapper)

## Mapper For Answer
class AnswerMapper(Mapper):
    id = RawField()
    question_id = RawField()
    content = RawField()
    state = RawField()
    created_by = RawField()
    updated_by = RawField()
    created_at = RawField()
    updated_at = RawField()

class ListAnswerMapper(Mapper):
    pass

## Mapper For Question
class QuestionMapper(Mapper):
    id = RawField()
    content = RawField()
    state = RawField()
    created_by = RawField()
    updated_by = RawField()
    created_at = RawField()
    updated_at = RawField()

    answers = ListDelegateField(AnswerMapper)

class ListQuestionMapper(Mapper):
    #question_list = ListDelegateField(QuestionMapper)
    result = ListDelegateField(QuestionMapper)


## Mapper For Inofrmation
class InformationMapper(Mapper):
    id = RawField()
    content = RawField()
    state = RawField()
    created_by = RawField()
    updated_by = RawField()
    created_at = RawField()
    updated_at = RawField()

class ListInformationMapper(Mapper):
    result = ListDelegateField(InformationMapper)

## Mapper For Tweet
class TweetMapper(Mapper):
    id = RawField()
    type = RawField()
    tweet_id = RawField()
    content = RawField()
    created_by = RawField()
    updated_by = RawField()
    created_at = RawField()
    updated_at = RawField()

class ListTweetMapper(Mapper):
    result = ListDelegateField(TweetMapper)

## Mapper For Response
class ResponseMapper(Mapper):
    id = RawField()
    type = RawField()
    content = RawField()
    state = RawField()
    created_by = RawField()
    updated_by = RawField()
    created_at = RawField()
    updated_at = RawField()

class ListResponseMapper(Mapper):
    result = ListDelegateField(ResponseMapper)

def clear_session():
    session.clear()
    pass

@app.route('/')
@crossdomain(origin='*')
def test():
    res = {1: 2}
    return jsonify(res)

@app.route('/operations', methods=['POST', 'OPTIONS'])
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

#@app.route('/operations', methods=['GET'])
@app.route('/operators', methods=['GET'])
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

#@app.route('/operations/<operation_id>', methods=['GET'])
@app.route('/operators/<operation_id>', methods=['GET'])
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
    operation = []
    res = Operation.query.filter("id = :operation_id").params(operation_id=operation_id).first()
    operation = Operation(id=operation_id,
                          username=res.username,
                          state=res.state,
                          created_at=res.created_at,
                          updated_at=res.updated_at
    )

    return operation

def get_operations():
    operations = []
    res = Operation.query.all()
    for row in res:
        operations.append(row)

    return operations

#@app.route('/operations/<operation_id>', methods=['PUT'])
@app.route('/operators/<operation_id>', methods=['PUT'])
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

@app.route('/operations/<operation_id>', methods=['DELETE'])
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

@app.route('/questions', methods=['GET'])
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
        logging.debug(questions)
        questions_dict = ListQuestionMapper({'result': questions}).as_dict()
    except:
        pass
    logging.debug(questions_dict)
    result = questions_dict['result']

    return jsonify(status_code=code, result=result)

# TODO answerも同時に登録するように修正すること
@app.route('/questions', methods=['POST'])
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

@app.route('/questions/<question_id>', methods=['GET'])
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
    res = Question.query.filter("id = :question_id").params(question_id=question_id).first()
    #logging.debug(res)
    question = Question(id=question_id,
                        content=res.content,
                        state=res.state,
                        created_by=res.created_by,
                        updated_by=res.updated_by,
                        created_at=res.created_at,
                        updated_at=res.updated_at
    )

    return question

def get_questions():
    """質問一覧のリストを返却する
    """
    questions = []
    res = Question.query.all()
    for row in res:
        # get_question(row["id"])でmodelをセットしていく？
        questions.append(row)

    return questions

@app.route('/questions/<question_id>', methods=['PUT'])
@crossdomain(origin='*')
def edit_question(question_id):
    """質問を更新します
    """
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    req = request.form
    try:
        row = db_session.query(Question).get(question_id)
        row.content = req['content']
        row.state = req['state']
        row.created_by = req['created_by']
        row.updated_by = req['updated_by']
        row.updated_at = tstr
        db_session.flush()
        #db_session.commit()
    except:
        pass
    finally:
        pass

    # app.logger.debug(request.form)
    return jsonify(status_code=code)

@app.route('/questions/<question_id>', methods=['DELETE'])
@crossdomain(origin='*')
def delete_question(question_id):
    """質問を削除します
    """
    code = 204
    try:
        row = Question.query.get(question_id)
        db_session.delete(row)
        db_session.flush()
    except:
        pass
    finally:
        pass

    #logging.debug(row.created_by)

    return jsonify(status_code=code)


# /answers
@app.route('/answers/<question_id>', methods=['POST'])
@crossdomain(origin='*')
def add_answer(question_id):
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    g.cursor.execute('insert into answers (question_id, content, state, created_by, updated_by, created_at, updated_at) values (%s, %s, %s, %s, %s, %s, %s)',
            ([question_id, request.form['content'], request.form['state'], request.form['created_by'], request.form['updated_by'], tstr, tstr]))
    g.connection.commit()

    return jsonify(status_code=code)

@app.route('/questions/<question_id>/answers', methods=['GET'])
@crossdomain(origin='*')
def index_answers(question_id):
    code = 200
    g.cursor.execute('select id, question_id, content, state, created_by, updated_by, created_at, updated_at from answers where question_id = %s',
            question_id)
    answers = [dict(id=row[0], question_id=row[1], content=row[2], state=row[3], created_by=row[4], updated_by=row[5], created_at=row[6], updated_at=row[7]) for row in g.cursor.fetchall()]

    return jsonify(status_code=code, result=answers)

@app.route('/answers/<answer_id>', methods=['GET'])
@crossdomain(origin='*')
def show_answer(answer_id):
    code = 200
    g.cursor.execute('select id, question_id, content, state, created_by, updated_by, created_at, updated_at from answers where id = %s',
            [answer_id])
    question = [dict(id=row[0], question_id=row[1], content=row[2], state=row[3], created_by=row[4], updated_by=row[5], created_at=row[6], updated_at=row[7]) for row in g.cursor.fetchall()]

    return jsonify(status_code=code, result=question)

@app.route('/answers/<answer_id>', methods=['PUT'])
@crossdomain(origin='*')
def edit_answer(answer_id):
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    g.cursor.execute('update answers set content = %s, state = %s, updated_by = %s, updated_at = %s where id = %s',
            ([request.form['content'], request.form['state'], request.form['updated_by'], tstr, answer_id]))
    g.connection.commit()

    return jsonify(status_code=code)

@app.route('/answers/<answer_id>', methods=['DELETE'])
@crossdomain(origin='*')
def delete_answer(answer_id):
    code = 204
    g.cursor.execute('delete from answers where id = %s',
    [answer_id])
    g.connection.commit()

    return jsonify(status_code=code)

@app.route('/informations', methods=['POST'])
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

@app.route('/informations', methods=['GET'])
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

@app.route('/informations/<information_id>', methods=['GET'])
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

@app.route('/informations/<information_id>', methods=['PUT'])
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

@app.route('/informations/<information_id>', methods=['DELETE'])
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

@app.route('/tweets', methods=['GET'])
@crossdomain(origin='*')
def index_tweets():
    """ツイート一覧を返します
    """
    code = 200
    tweets = []

    try:
        tweets = get_tweets()
        tweets_dict = ListTweetMapper({'result': tweets}).as_dict()
    except:
        pass

    result = tweets_dict['result']

    return jsonify(status_code=code, result=result)

# TODO pagingを実装する
def get_tweets():
    """dbからツイートを全件取得します
    """
    tweets = []
    res = Tweet.query.all()
    for row in res:
        tweets.append(row)

    return tweets

# TODO tweetを追加するapiの実装
# TODO filterの実装

@app.route('/responses', methods=['POST'])
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

@app.route('/responses', methods=['GET'])
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

@app.route('/responses/<response_id>', methods=['GET'])
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
    res = Response.query.filter("id = :response_id").params(response_id=response_id).first()
    response = Response(id=response_id,
                        type=res.type,
                        content=res.content,
                        state=res.state,
                        created_by=res.created_by,
                        updated_by=res.updated_by,
                        created_at=res.created_at,
                        updated_at=res.updated_at
    )

    return response

def get_responses():
    responses = []
    res = Response.query.all()
    for row in res:
        responses.append(row)

    return responses

@app.route('/responses/<response_id>', methods=['PUT'])
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

@app.route('/responses/<response_id>', methods=['DELETE'])
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

@app.route('/login', methods=['GET', 'POST'])
@crossdomain(origin='*')
def login():
    """ ログインします
    """
    code = 200
    error = None
    #logging.debug(request.form)

    if request.method == 'POST':
        #if request.form['username'] == app.config['USERNAME'] and request.form['password'] == app.config['PASSWORD']:
        if request.form['username'] == 'test' and request.form['password'] == 'pass':
            #session['logged_in'] = True
            set_username(request.form['username'])
            return redirect('/#/questions')
            #return jsonify(status_code=code)
        else:
            error = 'wrong'
            return redirect('/#/login')
            #return jsonify(error=error)

    return jsonify(status_code=code)

def set_username(username):
    session['username'] = username

def get_username():
    return session.get('username')

def is_login():
    return not not get_username()

def user_check():
    #logging.debug(is_login())
    if not is_login():
        logging.debug(is_login())
        abort(401)
        #return redirect('/#/login')

@app.route('/logout', methods=['GET'])
@crossdomain(origin='*')
def logout():
    """ ログアウトします
    """
    code = 200
    clear_session()
    return redirect('/#/login')
    #return jsonify(status_code=code)

if __name__ == '__main__':
    app.run()
