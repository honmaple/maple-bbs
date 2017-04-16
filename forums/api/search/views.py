#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-03-31 17:26:28 (CST)
# Last Update:星期日 2017-4-16 15:4:55 (CST)
#          By:
# Description:
# **************************************************************************
from flask import request, render_template
from forums.common.views import BaseMethodView as MethodView
from forums.api.topic.models import Topic
from forums.extension import search


class SearchView(MethodView):
    def get(self):
        query_dict = request.data
        keyword = query_dict.pop('keyword', None)
        include = query_dict.pop('include', '0')
        if keyword and len(keyword) >= 2:
            fields = None
            if include == '0':
                fields = ['title', 'content']
            elif include == '1':
                fields = ['title']
            elif include == '2':
                fields = ['content']
            results = search.whoosh_search(Topic, keyword, fields=fields)
            data = {'title': 'Search', 'results': results, 'keyword': keyword}
            return render_template('search/result.html', **data)
        data = {'title': 'Search'}
        return render_template('search/search.html', **data)
