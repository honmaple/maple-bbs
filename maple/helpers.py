#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: helpers.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 13:56:43 (CST)
# Last Update:星期四 2016-7-7 19:44:42 (CST)
#          By:
# Description:
# **************************************************************************
from flask import abort, current_app
from flask_login import current_user
from time import time
from random import randint
from maple import redis_data


def is_num(num):
    if num is not None:
        try:
            num = int(num)
            if num > 0:
                return num
            else:
                abort(404)
        except ValueError:
            abort(404)


def replies_page(topicId):
    app = current_app._get_current_object()
    replies = redis_data.hget('topic:%s' % str(topicId), 'replies')
    if not replies:
        replies = 0
    else:
        replies = int(replies)
    p = app.config['PER_PAGE']
    if replies % p == 0:
        q = replies // p
    else:
        q = replies // p + 1
    return q


def register_api(site, view, endpoint, url, pk='uid', pk_type='int'):
    view_func = view.as_view(endpoint)
    site.add_url_rule(url,
                      defaults={pk: None},
                      view_func=view_func,
                      methods=['GET', ])
    site.add_url_rule(url, view_func=view_func, methods=['POST', ])
    site.add_url_rule('%s<%s:%s>' % (url, pk_type, pk),
                      view_func=view_func,
                      methods=['GET', 'PUT', 'DELETE'])


def make_uid():
    a = str(int(time()))
    b = str(current_user.id).zfill(6)
    c = str(randint(10, 99))
    return a + b + c
