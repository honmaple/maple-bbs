#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: forums.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-17 13:12:23 (CST)
# Last Update:星期三 2017-3-29 21:5:42 (CST)
#          By:
# Description:
# **************************************************************************
from .views import BaseView
from forums.extension import db
from forums.api.forums.models import Board
from forums.api.tag.models import Tags


class BoardView(BaseView):
    form_excluded_columns = ('topics')


class TagView(BaseView):
    column_searchable_list = ['name']
    form_excluded_columns = ('topics', 'followers')


def register_forums(admin):
    admin.add_view(
        BoardView(
            Board,
            db.session,
            name='管理版块',
            endpoint='admin_board',
            category='管理社区'))
    admin.add_view(
        TagView(
            Tags,
            db.session,
            name='管理节点',
            endpoint='admin_tag',
            category='管理社区'))
