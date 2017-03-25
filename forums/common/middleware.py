#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: middleware.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-11-12 13:29:17 (CST)
# Last Update:星期六 2017-3-25 18:57:58 (CST)
#          By:
# Description:
# **************************************************************************
from flask import g, request
from flask_login import current_user
from forums.api.forums.forms import SortForm, SearchForm


class GlobalMiddleware(object):
    def preprocess_request(self):
        g.user = current_user
        g.sort_form = SortForm()
        g.search_form = SearchForm()
        request.user = current_user._get_current_object()
        if request.method == 'GET':
            request.data = request.args.to_dict()
        else:
            request.data = request.json
            if request.data is None:
                request.data = request.form.to_dict()
