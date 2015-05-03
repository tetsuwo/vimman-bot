#!/usr/bin/env python
# -*- coding: utf-8 -*-
from requests_oauthlib import OAuth1Session
from config.settings import *
import sys, json

c_k = Config['consumer_key']
c_s = Config['consumer_secret']
a_k = Config['access_token']
a_s = Config['access_token_secret']

MENSION_API_ENDPOINT = 'https://api.twitter.com/1.1/statuses/mentions_timeline.json'
UPDATE_API_ENDPOINT = 'https://api.twitter.com/1.1/statuses/update.json'

twitter = OAuth1Session(c_k, c_s, a_k, a_s)
reply_count = 0

raw_response = twitter.get(MENSION_API_ENDPOINT, params={})
if raw_response.status_code == 200:
    response = json.loads(raw_response.text)
    for tweet in response:
        res_tweet = '@%s wah gwaan' % (tweet['user']['screen_name'])

        request_params = {
            'status': res_tweet,
            'in_reply_to_status_id': tweet['user']['id_str']
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


