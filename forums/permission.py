#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: permission.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-03-28 16:02:43 (CST)
# Last Update:星期日 2017-4-2 11:47:33 (CST)
#          By:
# Description:
# **************************************************************************
from collections import namedtuple
from functools import partial, wraps

from flask import abort, current_app, flash, redirect, request, url_for
from flask_login import current_user, login_required
from flask_principal import (Need, Permission, RoleNeed, UserNeed,
                             identity_loaded)

super_permission = Permission(RoleNeed('super'))
confirm_permission = Permission(RoleNeed('confirmed')).union(super_permission)
auth_permission = Permission(RoleNeed('auth')).union(confirm_permission)
guest_permission = Permission(RoleNeed('guest')).union(auth_permission)

_TopicNeed = namedtuple('Topic', ['method', 'value'])
TopicNeed = partial(_TopicNeed, 'PUT')

_ReplyNeed = namedtuple('Reply', ['method', 'value'])
ReplyNeed = partial(_ReplyNeed, 'edit')

_CollectNeed = namedtuple('Collect', ['method', 'value'])
CollectNeed = partial(_CollectNeed, 'edit')


class TopicPermission(Permission):
    def __init__(self, pk):
        need = TopicNeed(pk)
        super(TopicPermission, self).__init__(need)


class ReplyPermission(Permission):
    def __init__(self, pk):
        need = ReplyNeed(pk)
        super(ReplyPermission, self).__init__(need)


class CollectPermission(Permission):
    def __init__(self, pk):
        need = CollectNeed(pk)
        super(CollectPermission, self).__init__(need)


def is_confirmed(func):
    @wraps(func)
    def _is_confirmed(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login', next=request.path))
        if confirm_permission.can():
            return func(*args, **kwargs)
        flash('请验证你的帐号', 'warning')
        return redirect(url_for('user.user', username=current_user.username))

    return _is_confirmed


def is_guest(func):
    @wraps(func)
    def _is_guest(*args, **kwargs):
        if not current_user.is_authenticated:
            return func(*args, **kwargs)
        flash('你已登陆，请勿重复登陆')
        return redirect('/')

    return _is_guest


class RestfulView(object):
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
                if isinstance(check, bool) and check:
                    return func(*args, **kwargs)
                elif check:
                    return check or self.callback()
            return func(*args, **kwargs)

        return decorator

    def callback(self):
        abort(403)
