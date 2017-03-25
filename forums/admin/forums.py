#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: forums.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-17 13:12:23 (CST)
# Last Update:星期六 2017-3-25 18:55:24 (CST)
#          By:
# Description:
# **************************************************************************
from .views import BaseView
from forums.extension import db
from forums.api.forums.models import Board


class BoardView(BaseView):
    pass


def register_forums(admin):
    admin.add_view(
        BoardView(
            Board,
            db.session,
            name='管理版块',
            endpoint='admin_board',
            category='管理社区'))
