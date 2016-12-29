#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: middleware.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-11-12 13:29:17 (CST)
# Last Update:星期四 2016-12-29 21:52:33 (CST)
#          By:
# Description:
# **************************************************************************
from flask import g
from flask_login import current_user
from api.forums.forms import SortForm, SearchForm


class GlobalMiddleware(object):
    def preprocess_request(self):
        g.user = current_user
        g.sort_form = SortForm()
        g.search_form = SearchForm()
