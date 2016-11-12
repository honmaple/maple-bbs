#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-07-15 18:40:33 (CST)
# Last Update:星期日 2016-11-13 0:11:41 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint, g, abort
from maple.forums.models import Board
from .views import BoardListView, BoardView

site = Blueprint('board', __name__)


@site.url_value_preprocessor
def pull_url(endpoint, values):
    g.parent_b = values.pop('parent_b', None)
    board = Board.query.filter_by(parent_board=g.parent_b).first()
    if board is None:
        abort(404)


@site.url_defaults
def add_url(endpoint, values):
    if 'parent_b' in values or not g.parent_b:
        return
    values['parent_b'] = g.parent_b


boardlist_view = BoardListView.as_view('boardlist')
board_view = BoardView.as_view('board')

site.add_url_rule('', view_func=boardlist_view)
site.add_url_rule('/<child_b>', view_func=board_view)
