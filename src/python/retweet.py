#!/usr/bin/env python
# -*- coding: utf-8 -*-
import twitter
import secret
import datetime

customer_key    = secret.dict['customer_key']
customer_secret = secret.dict['customer_secret']
access_token_key    = secret.dict['access_token_key']
access_token_secret = secret.dict['access_token_secret']


api = twitter.Api(customer_key,customer_secret,access_token_key,access_token_secret)

replies = api.GetReplies()
reply_text = '@%s reply %s' % (replies[0].user.screen_name, datetime.datetime.now())
reply_to = replies[0].id
api.PostUpdate(
  status=reply_text,
  in_reply_to_status_id=reply_to)

