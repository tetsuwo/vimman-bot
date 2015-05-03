#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

Config = {
    'secret_key': os.environ.get('SECRET_KEY'),
    'consumer_key': os.environ.get('TWITTER_CONSUMER_KEY'),
    'consumer_secret': os.environ.get('TWITTER_CONSUMER_SECRET'),
    'access_token': os.environ.get('TWITTER_ACCESS_TOKEN'),
    'access_token_secret': os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'),
    'api_url': os.environ.get('VIMMANBOT_API_URL'),
    'twitter_name': 'vimmanbot',
}
