#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: permission.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-06-09 19:53:35 (CST)
# Last Update:星期三 2016-6-15 17:50:37 (CST)
#          By:
# Description:
# **************************************************************************
from flask import (request, abort, current_app, redirect, jsonify, url_for,
                   flash, g)
from flask_principal import Permission, RoleNeed, UserNeed, identity_loaded
from flask_login import current_user, login_required
from maple import app
from collections import namedtuple
from functools import partial, wraps

TopicNeed = namedtuple('topic', ['method', 'value'])
EditTopicNeed = partial(TopicNeed, 'edit')


class EditTopicPermission(Permission):
    def __init__(self, topic_id):
        need = EditTopicNeed(topic_id)
        super(EditTopicPermission, self).__init__(need)


class BasePermission(object):
    decorators = ()

    def __call__(self, func):
        if self.decorators:
            for dec in self.decorators:
                return dec(func)

        @wraps(func)
        def decorator(*args, **kwargs):
            meth = getattr(self, request.method.lower(), None)
            if meth is None and request.method == 'HEAD':
                meth = getattr(self, 'get', None)
            assert meth is not None, 'Unimplemented method %r' % request.method
            check = meth(*args, **kwargs)
            if check:
                return check
            else:
                pass
            return func(*args, **kwargs)

        return decorator


class TopicPermission(BasePermission):
    @login_required
    def post(self):
        pass

    def get(self, uid):
        pass

    @login_required
    def put(self, uid):
        permission = EditTopicPermission(uid)
        if not permission.can():
            flash('你没有权限')
            return redirect(url_for('topic.topic', uid=uid))

    @login_required
    def delete(self):
        pass


class ReplyPermission(BasePermission):
    decorators = [login_required]

    def post(self, uid):
        pass

    def put(self, uid):
        pass

    def delete(self, uid):
        pass


class FollowPermission(BasePermission):
    decorators = [login_required]

    def get(self, type):
        pass

    def post(self, uid):
        pass

    def delete(self, uid):
        pass


class CollectPermission(BasePermission):
    decorators = [login_required]

    def get(self, type):
        pass

    def post(self, uid):
        pass

    def put(self, uid):
        pass

    def delete(self, uid):
        pass


class TagPermission(BasePermission):
    def get(self, tag):
        pass

    @login_required
    def post(self, tag):
        pass

    @login_required
    def put(self, tag):
        pass


class LikePermission(BasePermission):
    def post(self):
        if not g.user.is_authenticated:
            return jsonify(judge=False, url=url_for('auth.login'))

    def delete(self):
        if not g.user.is_authenticated:
            return jsonify(judge=False, url=url_for('auth.login'))


topic_permission = TopicPermission()
reply_permission = ReplyPermission()
follow_permission = FollowPermission()
collect_permission = CollectPermission()
tag_permission = TagPermission()
like_permission = LikePermission()

super_permission = Permission(RoleNeed('super'))


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    '''基础权限'''
    identity.user = current_user

    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.rolename))

    if hasattr(current_user, 'is_superuser'):
        if current_user.is_superuser:
            identity.provides.add(RoleNeed('super'))

    if hasattr(current_user, 'topics'):
        for topic in current_user.topics:
            identity.provides.add(EditTopicNeed(topic.id))
