#!/usr/bin/env python
# -*- coding: utf-8 -*-
from requests_oauthlib import OAuth1Session
import os, random, sys

consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')
access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

def fetch_questions():
    return

def get_questions():
    return [
        'Vim を保存しないで強制的に閉じるときは？',
        'Vim で画面を縦に分割するには？',
        'Vim のチュートリアルを開くには？',
    ]

API_ENDPOINT_URL = 'https://api.twitter.com/1.1/statuses/update.json'

questions = get_questions()
if len(questions) < 1:
    print('Not found questions')
    sys.exit(1)

params = {'status': random.choice(questions)}
twitter = OAuth1Session(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

raw_response = twitter.post(
    API_ENDPOINT_URL,
    params=params
)
if raw_response.status_code == 200:
    print('OK')
else:
    print('Error: %d' % raw_response.status_code)
