# -*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime as dt

from bpmappers import Mapper, RawField, DelegateField, ListDelegateField
# create base
engine = create_engine("mysql://root:@localhost:3306/vimmanbot",echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class Operation(Base):
    __tablename__ = 'operations'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    password = Column(String(50))
    salt = Column(String(50))
    state = Column(Integer)
    created_at = Column(DateTime, default=dt.now)
    updated_at = Column(DateTime, default=dt.now)

    def __init__(self, id, username, password, salt, state, created_at, updated_at):
        self.id = id
        self.username = username
        self.password = password
        self.salt = salt
        self.state = state
        self.created_at = created_at
        self.updated_at = updated_at

class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    state = Column(Integer)
    created_by = Column(String)
    updated_by = Column(String)
    created_at = Column(DateTime, default=dt.now)
    updated_at = Column(DateTime, default=dt.now)

    answers = relationship('Answer')
    
    def __init__(self, id, content, state, created_by, updated_by, created_at, updated_at):
        self.id = id
        self.content = content
        self.state = state
        self.created_by = created_by
        self.updated_by = updated_by
        self.created_at = created_at
        self.updated_at = updated_at

class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'))
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


class OperationMapper(Mapper):
    id = RawField()
    username = RawField()
    state = RawField()
    created_at = RawField()
    updated_at = RawField()

class ListOperationMapper(Mapper):
    result = ListDelegateField(OperationMapper)

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
