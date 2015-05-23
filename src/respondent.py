#!/usr/bin/env python
# -*- coding: utf-8 -*-

u""" 返答ボット

@vimmanbot 宛に届いたメンションについて返答するボット
1. tweets から tweet_id の最大値を得る
2. @vimmanbot 宛でかつ tweet_id より大きい ID のメンションを取得する
2.
"""

from requests_oauthlib import OAuth1Session
from config.settings import *
import sys, json

MENSION_API_ENDPOINT = 'https://api.twitter.com/1.1/statuses/mentions_timeline.json'
UPDATE_API_ENDPOINT = 'https://api.twitter.com/1.1/statuses/update.json'

twitter = OAuth1Session(
    Config['consumer_key'],
    Config['consumer_secret'],
    Config['access_token'],
    Config['access_token_secret']
)
reply_count = 0

raw_response = twitter.get(MENSION_API_ENDPOINT, params={})
if raw_response.status_code == 200:
    response = json.loads(raw_response.text)
    for tweet in response:
        if (tweet['user']['name'] == Config['twitter_name']):
            continue

        reply_status = '@%s wah gwaan' % (tweet['user']['screen_name'])

        request_params = {
            'status': reply_status,
            'in_reply_to_status_id': tweet['id_str']
        }
        tweet_raw_response = twitter.post(UPDATE_API_ENDPOINT, params=request_params)

        if tweet_raw_response.status_code == 200:
            print 'OK'
        else:
            print 'Error:', tweet_raw_response.status_code

        reply_count += 1
else:
    print 'Error:', raw_response.status_code

print 'REPLY COUNT:', reply_count


