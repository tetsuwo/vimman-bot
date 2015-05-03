#!/usr/bin/env python
# -*- coding: utf-8 -*-
from requests_oauthlib import OAuth1Session
from config.settings import *
import random, sys

def fetch_questions():
    return

def get_questions():
    return [
        'Vim を保存しないで強制的に閉じるときは？',
        'Vim で画面を縦に分割するには？',
        'Vim のチュートリアルを開くには？',
    ]

UPDATE_API_ENDPOINT = 'https://api.twitter.com/1.1/statuses/update.json'

questions = get_questions()
if len(questions) < 1:
    print('Not found questions')
    sys.exit(1)

request_params = {
    'status': random.choice(questions)
}
twitter = OAuth1Session(
    Config['consumer_key'],
    Config['consumer_secret'],
    Config['access_token'],
    Config['access_token_secret']
)

raw_response = twitter.post(
    UPDATE_API_ENDPOINT,
    params=request_params
)
if raw_response.status_code == 200:
    print('OK')
else:
    print('Error: %d' % raw_response.status_code)
