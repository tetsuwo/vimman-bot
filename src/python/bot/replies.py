#!/usr/bin/env python
# -*- coding: utf-8 -*-
from requests_oauthlib import OAuth1Session
import json
import secret

c_k = secret.dict['customer_key']
c_s = secret.dict['customer_secret']
a_k = secret.dict['access_token_key']
a_s = secret.dict['access_token_secret']

url = "https://api.twitter.com/1.1/statuses/mentions_timeline.json"

twitter = OAuth1Session(c_k, c_s, a_k, a_s)

params = {}

req = twitter.get(url, params = params)

if req.status_code == 200:
    timeline = json.loads(req.text)

    url = "https://api.twitter.com/1.1/statuses/update.json"
    for tweet in timeline:
        res_tweet = '@%s wah gwaan' % (tweet["user"]["screen_name"])
        params = {"status":res_tweet, "in_reply_to_status_id":tweet['user']["id_str"]}

        req = twitter.post(url, params = params)
        
        if req.status_code == 200:
            print ("OK")
        else:
            print ("Error: %d" % req.status_code)
else:
    # エラーの場合
    print ("Error: %d" % req.status_code)
