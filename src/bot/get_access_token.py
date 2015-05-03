#!/usr/bin/env python
#-*- coding: utf-8 -*-
from config.settings import *
import tweepy

consumer_key = Config['consumer_key']
consumer_secret = Config['consumer_secret']
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
print 'Access:', auth.get_authorization_url()
verifier = raw_input('Verifier:')
auth.get_access_token(verifier)
print 'Access Token:', auth.access_token
print 'Access Token Secret:', auth.access_token_secret
