# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify
from helpers.crossdomain import *
from models.model import *

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

# TODO tweetを追加するapiの実装
# TODO filterの実装
