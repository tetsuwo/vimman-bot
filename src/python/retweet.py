#!/usr/bin/env python
# -*- coding: utf-8 -*-
import twitter
import secret

customer_key    = secret.dict['customer_key']
customer_secret = secret.dict['customer_secret']
access_token_key    = secret.dict['access_token_key']
access_token_secret = secret.dict['access_token_secret']


api = twitter.Api(customer_key,customer_secret,access_token_key,access_token_secret)

retweet = api.GetReplies();

print retweet[0].user.screen_name

