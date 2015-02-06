# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify
from helpers.crossdomain import *
from models.model import *

from datetime import datetime as dt
import logging
LOG_FILENAME = 'example.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

app = Blueprint(__name__, "tweets")

@app.route('/', methods=['GET'])
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

# TODO created_by updated_byの取り扱いは未定
@app.route('/', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def add_tweet():
    """ ツイートログを追加します
    """
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    req = request.form

    #logging.debug(req)
    
    try:
        tweet = Tweet(
                id = None,
                type = req['tweets[type]'],
                tweet_id = req['tweets[tweet_id]'],
                content = req['tweets[content]'],
                post_url = req['tweets[post_url]'],
                created_by = 0,
                updated_by = 0,
                created_at = tstr,
                updated_at = tstr
        )
        db_session.add(tweet)
        db_session.flush()
        db_session.commit()
    except:
        pass
    finally:
        pass

    return jsonify(status_code=code)

# TODO filterの実装
