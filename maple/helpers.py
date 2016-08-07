#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: helpers.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 13:56:43 (CST)
# Last Update:星期日 2016-8-7 16:58:36 (CST)
#          By:
# Description:
# **************************************************************************
from flask import abort, current_app, Markup
from flask_login import current_user
from time import time
from random import randint
from maple import redis_data
from bleach import clean


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


def html_clean(text):
    tags = ['b', 'i', 'font', 'br']
    attrs = {'*': ['style', 'id', 'class'], 'font': ['color']}
    styles = ['color']
    return clean(text, tags=tags, attributes=attrs, styles=styles)


def replies_page(topicId):
    # app = current_app._get_current_object()
    replies = redis_data.hget('topic:%s' % str(topicId), 'replies')
    if not replies:
        replies = 0
    else:
        replies = int(replies)
    p = current_app.config['PER_PAGE']
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
    site.add_url_rule('%s/<%s:%s>' % (url, pk_type, pk),
                      view_func=view_func,
                      methods=['GET', 'PUT', 'DELETE'])


def make_uid():
    a = str(int(time()))
    b = str(current_user.id).zfill(6)
    c = str(randint(10, 99))
    return a + b + c


class ToJson(dict):
    def __init__(self, *args, **kwargs):
        super(ToJson, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(ToJson, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(ToJson, self).__delitem__(key)
        del self.__dict__[key]
