#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-03-13 13:29:37 (CST)
# Last Update: Wednesday 2019-05-08 14:24:25 (CST)
#          By:
# Description:
# **************************************************************************
from flask import (request, flash, redirect, url_for, render_template,
                   current_app)
from flask_login import login_required, current_user
from flask_maple.views import MethodView as _MethodView
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


class MethodView(_MethodView):
    @property
    def pageinfo(self):
        page = request.args.get('page', 1, type=int)
        if hasattr(self, 'per_page'):
            per_page = getattr(self, 'per_page')
        else:
            per_page = current_app.config.setdefault('PER_PAGE', 20)

        number = request.args.get('number', per_page, type=int)
        if number < -1:
            number = per_page
        if number > 100 or number == -1:
            number = 100
        return page, number

    def dispatch_request(self, *args, **kwargs):
        method = request.method
        meth = getattr(self, method.lower(), None)

        if meth is None and method == 'HEAD':
            meth = getattr(self, 'get', None)

        assert meth is not None, 'Unimplemented method %r' % request.method
        return meth(*args, **kwargs)

    def render_template(self, template, **kwargs):
        return render_template(template, **kwargs)


class BaseMethodView(_MethodView):
    @cache.cached(timeout=180, key_prefix=cache_key)
    def dispatch_request(self, *args, **kwargs):
        return super(BaseMethodView, self).dispatch_request(*args, **kwargs)

    def render_template(self, template, **kwargs):
        return render_template(template, **kwargs)

    def render(self, template, **kwargs):
        return render_template(template, **kwargs)


class IsAuthMethodView(BaseMethodView):
    decorators = [login_required]


class IsConfirmedMethodView(BaseMethodView):
    decorators = [is_confirmed, login_required]
