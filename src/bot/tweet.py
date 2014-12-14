#!/usr/bin/env python
# -*- coding: utf-8 -*-
from requests_oauthlib import OAuth1Session
import secret
import random

def tweet_list():
    return [
        'Vim を保存しないで強制的に閉じるときは？',
        'Vim で画面を縦に分割するには？',
        'Vim のチュートリアルを開くには？',
    ]

url = "https://api.twitter.com/1.1/statuses/update.json"

lists = tweet_list()
post_tweet = random.choice(lists) 

params = {"status": post_tweet}

twitter = OAuth1Session(c_k, c_s, a_k, a_s)
req = twitter.post(url, params = params)

if req.status_code == 200:
    print ("OK")
else:
    print ("Error: %d" % req.status_code)

