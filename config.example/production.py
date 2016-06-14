#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: config.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 12:31:46 (CST)
# Last Update:星期二 2016-6-14 23:42:32 (CST)
#          By: jianglin
# Description:
# **************************************************************************
from datetime import timedelta

DEBUG = True
SECRET_KEY = ''
SECURITY_PASSWORD_SALT = ''

PERMANENT_SESSION_LIFETIME = timedelta(days=3)
REMEMBER_COOKIE_DURATION = timedelta(days=3)

PER_PAGE = 12

# 定制缓存 = 60
CACHE_DEFAULT_TIMEOUT = 60
CACHE_KEY_PREFIX = 'cache:'
CACHE_REDIS_HOST = '127.0.0.1'
CACHE_REDIS_PORT = ''
CACHE_REDIS_PASSWORD = ''
CACHE_REDIS_DB = 1

# REDIS_PASSWORD = 'redis'
# REDIS_DB = 1

ONLINE_LAST_MINUTES = 5

MAIL_SERVER = ''
MAIL_PORT =
MAIL_USE_TLS =
MAIL_USE_SSL =
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAIL_DEFAULT_SENDER = ''

# SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = ''
