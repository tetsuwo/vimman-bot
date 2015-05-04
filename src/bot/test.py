#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, json, requests
from config.settings import *

r = requests.get('http://www.vimmanbot.local/api/informations/')
print r.status_code


