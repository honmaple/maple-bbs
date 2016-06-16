#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-06-03 14:32:06 (CST)
# Last Update:星期五 2016-6-17 14:0:47 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint, g, render_template, abort, request
from maple.helpers import is_num
from maple.topic.models import Topic
from maple.forums.models import Board

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


@site.route('', defaults={'child_b': None})
@site.route('/<child_b>')
def board(child_b):
    page = is_num(request.args.get('page'))
    if child_b is None:
        boards = Board.query.filter_by(parent_board=g.parent_b).all()
        topics = Topic.query.join(Topic.board).filter(
            Board.parent_board == g.parent_b).paginate(page, 20, True)
        data = {'boards': boards, 'topics': topics}
        return render_template('forums/board_list.html', **data)
    else:
        board = Board.query.filter_by(board=child_b).first_or_404()
        topics = board.topics.paginate(page, 20, True)
        data = {'board': board, 'topics': topics}
        return render_template('forums/board.html', **data)
