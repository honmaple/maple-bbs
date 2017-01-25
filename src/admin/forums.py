#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: forums.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-17 13:12:23 (CST)
# Last Update:星期三 2017-1-25 20:22:51 (CST)
#          By:
# Description:
# **************************************************************************
from .views import BaseView
from forums.extension import db
from api.board.models import Board


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
