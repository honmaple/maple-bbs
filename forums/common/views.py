#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-10-25 20:57:36 (CST)
# Last Update:星期四 2016-12-29 20:54:44 (CST)
#          By:
# Description:
# **************************************************************************
from flask import (current_app, request)

__all__ = ['ViewListMixin']


class ViewListMixin(object):
    @property
    def page_info(self):
        page = request.args.get('page', 1, type=int)
        if hasattr(self, 'per_page'):
            per_page = getattr(self, 'per_page')
            number = request.args.get('number', per_page, type=int)
        else:
            per_page = current_app.config.setdefault('PER_PAGE', 20)
            number = request.args.get('number', per_page, type=int)
        if number > 100:
            number = current_app.config['PER_PAGE']
        return page, number

    @property
    def filter_dict(self):
        return {}

    @property
    def order_by(self):
        return ()
