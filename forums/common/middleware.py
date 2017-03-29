#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: middleware.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-11-12 13:29:17 (CST)
# Last Update:星期三 2017-3-29 13:29:17 (CST)
#          By:
# Description:
# **************************************************************************
from flask import g, request
from flask_login import current_user
from forums.api.forms import SortForm, SearchForm


def set_form(form):
    within = request.args.get('within', 0, type=int)
    orderby = request.args.get('orderby', 0, type=int)
    desc = request.args.get('desc', 0, type=int)
    form.within.data = within
    form.orderby.data = orderby
    form.desc.data = desc
    return form


class GlobalMiddleware(object):
    def preprocess_request(self):
        g.user = current_user
        g.sort_form = SortForm()
        g.sort_form = set_form(g.sort_form)
        g.search_form = SearchForm()
        request.user = current_user._get_current_object()
        if request.method == 'GET':
            request.data = request.args.to_dict()
        else:
            request.data = request.json
            if request.data is None:
                request.data = request.form.to_dict()
