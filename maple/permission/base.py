#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: base.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-07-16 15:25:16 (CST)
# Last Update:星期日 2016-8-7 14:0:7 (CST)
#          By:
# Description:
# **************************************************************************
from flask_principal import RoleNeed, UserNeed, identity_loaded
from flask_login import current_user
from flask import request, abort
from maple import app
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


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    '''基础权限'''
    identity.user = current_user

    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.name))

    if hasattr(current_user, 'is_superuser'):
        if current_user.is_superuser:
            identity.provides.add(RoleNeed('super'))

    if hasattr(current_user, 'topics'):
        for topic in current_user.topics:
            identity.provides.add(EditTopicNeed(topic.uid))

    if hasattr(current_user, 'collects'):
        for collect in current_user.collects:
            identity.provides.add(GetCollect(collect.id))
            identity.provides.add(PostCollect(collect.id))

    # if hasattr(current_user, 'likes'):
    #     for like in current_user.likes:
    #         identity.provides.add(GetLike(like.id))
