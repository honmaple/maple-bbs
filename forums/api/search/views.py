#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-03-31 17:26:28 (CST)
# Last Update:星期五 2017-3-31 17:48:23 (CST)
#          By:
# Description:
# **************************************************************************
from flask import request
from forums.common.views import BaseMethodView as MethodView
from forums.api.topic.models import Topic


class SearchView(MethodView):
    def get(self):
        query_dict = request.data
        search = query_dict.pop('key', None)
        results = Topic.query.whoosh_search('第一').all()
        print(results)
        return ''

    def post(self):
        pass
