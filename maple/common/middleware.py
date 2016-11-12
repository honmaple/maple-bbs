#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: middleware.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-11-12 20:34:27 (CST)
# Last Update:星期六 2016-11-12 21:19:18 (CST)
#          By:
# Description:
# **************************************************************************
from flask import request, g
from flask_login import current_user
from maple.forums.forms import SortForm, SearchForm
from maple.main.records import mark_online


class CommonMiddleware(object):
    def __call__(self, **kwargs):
        g.user = current_user
        g.sort_form = SortForm()
        g.search_form = SearchForm()


class OnlineMiddleware(object):
    def __call__(self, **kwargs):
        if g.user.is_authenticated:
            mark_online(g.user.username)
        else:
            mark_online(request.remote_addr)
        g.get_online = get_online()


def get_online():
    from maple.main.records import load_online_users
    return (load_online_users(1), load_online_users(2), load_online_users(3),
            load_online_users(4), load_online_users(5))
