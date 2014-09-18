#!/usr/bin/env python
# -*- coding: utf-8 -*-
import twitter
import secret
import random

def tweet_list():
    return [
        'Vim を保存しないで強制的に閉じるときは？',
        'Vim で画面を縦に分割するには？',
        'Vim のチュートリアルを開くには？',
    ]

lists = tweet_list()
post_tweet = random.choice(lists) 

customer_key    = secret.dict['customer_key']
customer_secret = secret.dict['customer_secret']
access_token_key    = secret.dict['access_token_key']
access_token_secret = secret.dict['access_token_secret']


api = twitter.Api(customer_key,customer_secret,access_token_key,access_token_secret)
api.PostUpdates(post_tweet.decode('utf-8'))
