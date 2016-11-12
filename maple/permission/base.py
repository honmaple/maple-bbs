#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: base.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-07-16 15:25:16 (CST)
# Last Update:星期六 2016-11-12 20:40:43 (CST)
#          By:
# Description:
# **************************************************************************
from flask_principal import RoleNeed, UserNeed, identity_loaded
from flask_login import current_user
from flask import request, abort
from functools import wraps
from .permission import EditTopicNeed, GetCollect, PostCollect


class RestBase(object):
    decorators = ()

    def __call__(self, func):
        f = self.method(func)
        if self.decorators:
            for dec in reversed(self.decorators):
                f = dec(f)
        return f

    def method(self, func):
        @wraps(func)
        def decorator(*args, **kwargs):
            meth = getattr(self, request.method.lower(), None)
            if request.method == 'HEAD':
                meth = getattr(self, 'get', None)
            if meth is not None:
                check = meth(*args, **kwargs)
                if check:
                    return self.callback()
            return func(*args, **kwargs)

        return decorator

    def callback(self):
        abort(403)
