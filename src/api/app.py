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

@app.before_request
def before_request():
    pass
    #g.engine = create_engine("mysql://root:@localhost:3306/vimmanbot",echo=True)
    #g.connection = g.engine.connect()


    #user_check()
    
    #g.connection = MySQLdb.connect(
    #    host=db_config["host"],
    #    db=db_config["db"],
    #    user=db_config["user"],
    #    passwd=db_config["passwd"],
    #    port=db_config["port"],
    #    unix_socket=db_config["unix_socket"]
    #)
    #g.cursor = g.connection.cursor()


@app.teardown_request
def teardown_request(exception):
    pass
    #cursor = getattr(g, 'cursor', None)
    #if cursor is not None:
    #    cursor.close()

    #connection = getattr(g, 'connection', None)
    #if connection is not None:
    #    connection.close()

# モデルクラス TODO 外部に出す
# operationsクラス
class Operation(Base):
    __tablename__ = 'operations'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    password = Column(String(50))
    salt = Column(String(50))
    state = Column(Integer)
    created_at = Column(DateTime, default=dt.now)
    updated_at = Column(DateTime, default=dt.now)

    def __init__(self, id, username, salt, state, created_at, updated_at):
        self.id = id
        self.username = username
        self.salt = salt
        self.state = state
        self.created_at = created_at
        self.updated_at = updated_at

# questionsテーブルのmodel
class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    state = Column(Integer)
    created_by = Column(String)
    updated_by = Column(String)
    created_at = Column(DateTime, default=dt.now)
    updated_at = Column(DateTime, default=dt.now)
    
    def __init__(self, id, content, state, created_by, updated_by, created_at, updated_at):
        self.id = id
        self.content = content
        self.state = state
        self.created_by = created_by
        self.updated_by = updated_by
        self.created_at = created_at
        self.updated_at = updated_at

# answersクラス
class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer)
    content = Column(String)
    state = Column(Integer)
    created_by = Column(String(50))
    updated_by = Column(String(50))
    created_at = Column(DateTime, default=dt.now)
    updated_at = Column(DateTime, default=dt.now)

    def __init__(self, id, question_id, content, state, created_by, updated_by, created_at, updated_at):
        self.id = id
        self.question_id = question_id
        self.content = content
        self.state = state
        self.created_by = created_by
        self.updated_by = updated_by
        self.created_at = created_at
        self.updated_at = updated_at

# informationsクラス
class Information(Base):
    __tablename__ = 'informations'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    state = Column(Integer)
    created_by = Column(String(50))
    updated_by = Column(String(50))
    created_at = Column(DateTime, default=dt.now)
    updated_at = Column(DateTime, default=dt.now)

    def __init__(self, id, content, state, created_by, updated_by, created_at, updated_at):
        self.id = id
        self.content = content
        self.state = state
        self.created_by = created_by
        self.updated_by = updated_by
        self.created_at = created_at
        self.updated_at = updated_at

# tweetsクラス
class Tweet(Base):
    __tablename__ = 'tweets' 
    id = Column(Integer, primary_key=True)
    type = Column(String(10))
    tweet_id = Column(Integer)
    content = Column(String)
    created_by = Column(String(50))
    updated_by = Column(String(50))
    created_at = Column(DateTime, default=dt.now)
    updated_at = Column(DateTime, default=dt.now)

    def __init__(self, id, type, tweet_id, content, created_by, updated_by, created_at, updated_at):
        self.id = id
        self.type = type
        self.tweet_id = tweet_id
        self.content = content
        self.created_by = created_by
        self.updated_by = updated_by
        self.created_at = created_at
        self.updated_at = updated_at

# responsesクラス
class Response(Base):
    __tablename__ = 'responses' 
    id = Column(Integer, primary_key=True)
    type = Column(String(10))
    content = Column(String)
    state = Column(Integer)
    created_by = Column(String(50))
    updated_by = Column(String(50))
    created_at = Column(DateTime, default=dt.now)
    updated_at = Column(DateTime, default=dt.now)

    def __init__(self, id, type, content, state, created_by, updated_by, crated_at, updated_at):
        self.id = id
        self.type = type
        self.content = content
        self.state = state
        self.created_by = created_by
        self.updated_by = updated_by
        self.created_at = created_at
        self.updated_at = updated_at

# マッパークラス TODO 外に出すこと
## Mapper For Operation
class OperationMapper(Mapper):
    id = RawField()
    state = RawField()
    created_at = RawField()
    updated_at = RawField()

class ListOperationMapper(Mapper):
    result = ListDelegateField(OperationMapper)

## Mapper For Question
class QuestionMapper(Mapper):
    id = RawField()
    content = RawField()
    state = RawField()
    created_by = RawField()
    updated_by = RawField()
    created_at = RawField()
    updated_at = RawField()

class ListQuestionMapper(Mapper):
    #question_list = ListDelegateField(QuestionMapper)
    result = ListDelegateField(QuestionMapper)

## Mapper For Answer
class AnswerMapper(Mapper):
    pass

class ListAnswerMapper(Mapper):
    pass

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
    pass

class ListResponseMapper(Mapper):
    pass

def clear_session():
    session.clear()
    pass

@app.route('/')
@crossdomain(origin='*')
def test():
    res = {1: 2}
    return jsonify(res)

# /operations
@app.route('/operations', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def add_operation():
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    # TODO saltのセット方法
    g.cursor.execute('insert into operations (username, password, salt, state, created_at, updated_at) values (%s,%s,%s,%s,%s,%s)',
            ([request.form['username'], request.form['password'], "salt1", request.form['state'], tstr, tstr]))
    g.connection.commit()

    return jsonify(status_code=code)

@app.route('/operations', methods=['GET'])
@crossdomain(origin='*')
def index_operatinos():
    code = 200
    # TODO passwordを外す
    # cur = g.db.execute('select id, username, password, state, created_at, updated_at from operations')
    g.cursor.execute('select id, username, password, state, created_at, updated_at from operations')
    operations = g.cursor.fetchall()

    # print operations
    #operations = [dict(id=row[0], username=row[1], password=row[2], state=row[3], created_at=row[4], updated_at=row[5]) for row in g.cursor.fetchall()]
    operations = [dict(id=row[0], username=row[1], password=row[2], state=row[3], created_at=row[4], updated_at=row[5]) for row in operations]
    # app.logger.debug(questions)
    # operations = 200
    return jsonify(status_code=code, result=operations)

@app.route('/operations/<operation_id>', methods=['GET'])
@crossdomain(origin='*')
def show_operation(operation_id):
    code = 200
    g.cursor.execute('select id, username, password, state, created_at, updated_at from operations where id = %s',
            [operation_id])
    operation = [dict(id=row[0], username=row[1], password=row[2], state=row[3], created_at=row[4], updated_at=row[5]) for row in g.cursor.fetchall()]

    return jsonify(status_code=code, result=operation)

@app.route('/operations/<operation_id>', methods=['PUT'])
@crossdomain(origin='*')
def edit_operation(operation_id):
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    g.cursor.execute('update operations set username = %s, password = %s, state = %s, updated_at = %s where id = %s',
            ([request.form['username'], request.form['password'], request.form['state'], tstr, operation_id]))
    g.connection.commit()

    return jsonify(status_code=code)

@app.route('/operations/<operation_id>', methods=['DELETE'])
@crossdomain(origin='*')
def delete_operation(operation_id):
    code = 204
    g.cursor.execute('delete from operations where id = %s',
    ([operation_id]))
    g.connection.commit()

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

    try:
        questions = get_questions()
        questions_dict = ListQuestionMapper({'result': questions}).as_dict()
    except:
        pass

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

# /informations
@app.route('/informations', methods=['POST'])
@crossdomain(origin='*')
def add_information():
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    g.cursor.execute('insert into informations (content, state, created_by, updated_by, created_at, updated_at) values (%s, %s, %s, %s, %s, %s)',
            [request.form['content'], request.form['state'], request.form['created_by'], request.form['updated_by'], tstr, tstr])
    g.connection.commit()

    return jsonify(status_code=code)

@app.route('/informations', methods=['GET'])
@crossdomain(origin='*')
def index_informations():
    code = 200
    g.cursor.execute('select id, content, state, created_by, updated_by, created_at, updated_at from informations')
    informations = [dict(id=row[0], content=row[1], state=row[2], created_by=row[3], updated_by=row[4], created_at=row[5], updated_at=row[6]) for row in g.cursor.fetchall()]
    # app.logger.debug(questions)
    return jsonify(status_code=code, result=informations)

@app.route('/informations/<information_id>', methods=['GET'])
@crossdomain(origin='*')
def show_information(information_id):
    code = 200
    g.cursor.execute('select id, content, state, created_by, updated_by, created_at, updated_at from informations where id = %s',
            [information_id])
    information = [dict(id=row[0], content=row[1], state=row[2], created_by=row[3], updated_by=row[4], created_at=row[5], updated_at=row[6]) for row in g.cursor.fetchall()]

    return jsonify(status_code=code, result=information)

@app.route('/informations/<information_id>', methods=['PUT'])
@crossdomain(origin='*')
def edit_information(information_id):
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    g.cursor.execute('update informations set content = %s, state = %s, updated_by = %s, updated_at = %s where id = %s',
            ([request.form['content'], request.form['state'], request.form['updated_by'], tstr, information_id]))
    g.connection.commit()

    return jsonify(status_code=code)

@app.route('/informations/<information_id>', methods=['DELETE'])
@crossdomain(origin='*')
def delete_information(information_id):
    code = 204
    g.cursor.execute('delete from informations where id = %s',
    [information_id])
    g.connection.commit()

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

# /responses
@app.route('/responses', methods=['POST'])
@crossdomain(origin='*')
def add_response():
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    g.cursor.execute('insert into responses (type, content, state, created_by, updated_by, created_at, updated_at) values (%s, %s, %s, %s, %s, %s, %s)',
            ([request.form['type'], request.form['content'], request.form['state'], request.form['created_by'], request.form['updated_by'], tstr, tstr]))
    g.connection.commit()

    return jsonify(status_code=code)

@app.route('/responses', methods=['GET'])
@crossdomain(origin='*')
def index_responses():
    code = 200
    g.cursor.execute('select id, type, content, state, created_by, updated_by, created_at, updated_at from responses')
    responses = [dict(id=row[0], type=row[1], content=row[2], state=row[3], created_by=row[4], updated_by=row[5], created_at=row[6], updated_at=row[7]) for row in g.cursor.fetchall()]
    # app.logger.debug(questions)
    return jsonify(status_code=code, result=responses)

@app.route('/responses/<response_id>', methods=['GET'])
@crossdomain(origin='*')
def show_response(response_id):
    code = 200
    g.cursor.execute('select id, type, content, state, created_by, updated_by, created_at, updated_at from responses where id = %s',
            [response_id])
    response = [dict(id=row[0], type=row[1], content=row[2], state=row[3], created_by=row[4], updated_by=row[5], created_at=row[6], updated_at=row[7]) for row in g.cursor.fetchall()]

    return jsonify(status_code=code, result=response)

@app.route('/responses/<response_id>', methods=['PUT'])
@crossdomain(origin='*')
def edit_response(response_id):
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    g.cursor.execute('update responses set type = %s, content = %s, state = %s, updated_by = %s, updated_at = %s where id = %s',
            ([request.form['type'], request.form['content'], request.form['state'], request.form['updated_by'], tstr, response_id]))
    g.connection.commit()

    return jsonify(status_code=code)

@app.route('/responses/<response_id>', methods=['DELETE'])
@crossdomain(origin='*')
def delete_response(response_id):
    code = 204
    g.cursor.execute('delete from responses where id = %s',
    [response_id])
    g.connection.commit()

    return jsonify(status_code=code)

# /login
@app.route('/login', methods=['GET', 'POST'])
@crossdomain(origin='*')
def login():
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

# /logout
@app.route('/logout', methods=['GET'])
@crossdomain(origin='*')
def logout():
    code = 200
    clear_session()
    return redirect('/#/login')
    #return jsonify(status_code=code)

if __name__ == '__main__':
    app.run()
