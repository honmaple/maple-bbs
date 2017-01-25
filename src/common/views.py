#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-10-25 20:57:36 (CST)
# Last Update:星期三 2017-1-25 21:55:25 (CST)
#          By:
# Description:
# **************************************************************************
from flask import (current_app, request)
from flask.views import MethodView
from flask_login import login_required
from .utils import log_exception


class BaseMethodView(MethodView):
    # @log_exception
    def dispatch_request(self, *args, **kwargs):
        return super(BaseMethodView, self).dispatch_request(*args, **kwargs)

    @property
    def page_info(self):
        page = request.args.get('page', 1, type=int)
        if hasattr(self, 'per_page'):
            per_page = getattr(self, 'per_page')
        else:
            per_page = current_app.config.setdefault('PER_PAGE', 20)

        number = request.args.get('number', per_page, type=int)
        if number > 100:
            number = current_app.config['PER_PAGE']
        return page, number

    def filter_dict(self, model):
        return {}

    def order_by(self, model):
        return ()


class IsAuthMethodView(BaseMethodView):
    decorators = [login_required]


class IsAdminMethodView(BaseMethodView):
    decorators = [login_required]


class IsSuperAdminMethodView(BaseMethodView):
    decorators = [login_required]
