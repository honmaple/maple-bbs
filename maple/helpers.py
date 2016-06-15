#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: helpers.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 13:56:43 (CST)
# Last Update:星期三 2016-6-15 18:46:40 (CST)
#          By:
# Description:
# **************************************************************************
from flask import abort
from flask_login import current_user
from time import time
from random import randint


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
