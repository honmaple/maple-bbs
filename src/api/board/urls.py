#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-15 22:28:28 (CST)
# Last Update:星期三 2017-1-25 21:54:40 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint
from .views import BoardListView, BoardView

site = Blueprint('board', __name__)

board_list = BoardListView.as_view('list')
board = BoardView.as_view('board')
forums = BoardListView.as_view('forums')

site.add_url_rule('/index', view_func=forums)
site.add_url_rule('/forums', view_func=board_list)
site.add_url_rule('/forums/<int:boardId>', view_func=board)
