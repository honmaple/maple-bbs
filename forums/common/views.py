#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-03-13 13:29:37 (CST)
# Last Update:星期五 2017-4-21 17:54:23 (CST)
#          By:
# Description:
# **************************************************************************
from flask import request, current_app, flash, redirect, url_for
from flask.views import MethodView
from flask_login import login_required, current_user
from forums.permission import confirm_permission
from forums.extension import cache


def cache_key():
    return 'view:{}:{}'.format(request.remote_addr, request.url)


def is_confirmed(func):
    def _is_confirmed(*args, **kwargs):
        if confirm_permission.can():
            ret = func(*args, **kwargs)
            return ret
        flash('请验证你的帐号', 'warning')
        return redirect(url_for('user.user', username=current_user.username))

    return _is_confirmed


class BaseMethodView(MethodView):
    @property
    def page_info(self):
        page = request.args.get('page', 1, type=int)
        if hasattr(self, 'per_page'):
            per_page = getattr(self, 'per_page')
        else:
            per_page = current_app.config.setdefault('PER_PAGE', 20)

        number = request.args.get('number', per_page, type=int)
        if number > 100:
            number = per_page
        return page, number

    @cache.cached(timeout=180, key_prefix=cache_key)
    def dispatch_request(self, *args, **kwargs):
        return super(BaseMethodView, self).dispatch_request(*args, **kwargs)


class IsAuthMethodView(BaseMethodView):
    decorators = [login_required]


class IsConfirmedMethodView(BaseMethodView):
    decorators = [is_confirmed, login_required]
