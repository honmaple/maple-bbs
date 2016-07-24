#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: permission.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-07-16 16:40:53 (CST)
# Last Update:星期日 2016-7-24 20:38:50 (CST)
#          By:
# Description:
# **************************************************************************
from flask import (redirect, url_for, flash, request)
from flask_login import login_required, current_user
from maple.permission.base import RestBase
from maple.permission.permission import EditTopicNeed
from flask_principal import Permission, RoleNeed
from flask_babelex import gettext as _
from functools import wraps


class TopicPermission(RestBase):
    def get(self, topicId):
        order = request.args.get('orderby')
        if topicId is None:
            if order:
                return True
        else:
            if order and order not in ['time', 'like']:
                return True

    @login_required
    def post(self):
        def callback():
            flash(
                _("You haven't confirm your account,Please confirmed"),
                'warning')
            return redirect(url_for('user.user',
                                    user_url=current_user.username))

        permission = Permission(RoleNeed('confirmed'))
        if not permission.can():
            self.callback = callback
            return True

    @login_required
    def put(self, topicId):
        def callback():
            flash(_("You have no permission"), 'warning')
            return redirect(url_for('topic.topic', topicId=topicId))

        permission = Permission(EditTopicNeed(topicId))
        if not permission.can():
            self.callback = callback
            return True

    @login_required
    def delete(self, topicId):
        return True


class ReplyPermission(RestBase):
    decorators = [login_required]

    def post(self, topicId):
        permission = Permission(RoleNeed('confirmed'))
        if not permission.can():
            return True

    def callback(self):
        flash(
            _("You haven't confirm your account,Please confirmed"),
            'warning')
        return redirect(url_for('user.user', user_url=current_user.username))


def tag_permission(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        permission = Permission(RoleNeed('confirmed'))
        if not permission.can():
            flash(
                _("You haven't confirm your account,Please confirmed"),
                'warning')
            return redirect(url_for('user.user',
                                    user_url=current_user.username))
        return func(*args, **kwargs)

    return decorator

preview_permission = tag_permission
topic_permission = TopicPermission()
reply_permission = ReplyPermission()
