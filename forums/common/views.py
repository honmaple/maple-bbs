#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-03-13 13:29:37 (CST)
# Last Update: Sunday 2018-03-04 22:37:00 (CST)
#          By:
# Description:
# **************************************************************************
from flask import (request, flash, redirect, url_for, render_template)
from flask_login import login_required, current_user
from flask_maple.views import MethodView
from forums.permission import confirm_permission
from forums.extension import cache


def cache_key():
    if current_user.is_authenticated:
        return 'view:{}:{}'.format(current_user.id, request.url)
    return 'view:{}'.format(request.url)


def is_confirmed(func):
    def _is_confirmed(*args, **kwargs):
        if confirm_permission.can():
            ret = func(*args, **kwargs)
            return ret
        flash('请验证你的帐号', 'warning')
        return redirect(url_for('user.user', username=current_user.username))

    return _is_confirmed


class BaseMethodView(MethodView):
    @cache.cached(timeout=180, key_prefix=cache_key)
    def dispatch_request(self, *args, **kwargs):
        return super(BaseMethodView, self).dispatch_request(*args, **kwargs)

    def render_template(self, template, **kwargs):
        return render_template(template, **kwargs)


class IsAuthMethodView(BaseMethodView):
    decorators = [login_required]


class IsConfirmedMethodView(BaseMethodView):
    decorators = [is_confirmed, login_required]
