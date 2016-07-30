#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-06-03 14:32:06 (CST)
# Last Update:星期六 2016-7-30 22:13:1 (CST)
#          By:
# Description:
# **************************************************************************
from flask import g, render_template, request
from maple.helpers import is_num
from maple.topic.models import Topic
from maple.forums.models import Board


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
