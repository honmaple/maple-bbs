#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-06-03 14:32:06 (CST)
# Last Update:星期一 2016-7-4 17:41:42 (CST)
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
        topic_base = Topic.query.join(Topic.board).filter(Board.parent_board ==
                                                          g.parent_b)
        topics = topic_base.filter(Topic.is_top == False).paginate(page, 20,
                                                                   True)
        top_topics = topic_base.filter(Topic.is_top == True).limit(5).all()
        data = {'title': '%s - ' % g.parent_b,
                'boards': boards,
                'topics': topics,
                'top_topics': top_topics}
        return render_template('board/board_list.html', **data)
    else:
        board = Board.query.filter_by(board=child_b).first_or_404()
        topic_base = board.topics
        topics = topic_base.filter(Topic.is_top == False).paginate(page, 20,
                                                                   True)
        top_topics = topic_base.filter(Topic.is_top == True).limit(5).all()
        data = {'title': '%s - ' % board.board,
                'board': board,
                'topics': topics,
                'top_topics': top_topics}
        return render_template('board/board.html', **data)
