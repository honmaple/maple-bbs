#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-17 20:45:08 (CST)
# Last Update:星期四 2017-3-30 14:54:26 (CST)
#          By:
# Description:
# **************************************************************************
from flask import render_template, request
from flask_babelex import gettext as _

from forums.api.topic.models import Topic
from forums.common.views import BaseMethodView as MethodView
from forums.common.utils import (gen_filter_dict, gen_order_by)

from .models import Board


class IndexView(MethodView):
    def get(self):
        topics = Topic.query.filter_by(
            is_good=True, is_top=False).paginate(1, 10)
        top_topics = Topic.query.filter_by(is_top=True).limit(5)
        if not topics.items:
            topics = Topic.query.filter_by(is_top=False).paginate(1, 10)
        data = {'title': '', 'topics': topics, 'top_topics': top_topics}
        return render_template('forums/index.html', **data)


class AboutView(MethodView):
    def get(self):
        data = {'title': _('About - ')}
        return render_template('forums/about.html', **data)


class HelpView(MethodView):
    def get(self):
        data = {'title': _('Help - ')}
        return render_template('forums/help.html', **data)


class ContactView(MethodView):
    def get(self):
        data = {'title': _('Contact - ')}
        return render_template('forums/contact.html', **data)


class BoardListView(MethodView):
    def get(self):
        query_dict = request.data
        page, number = self.page_info
        keys = ['name']
        order_by = gen_order_by(query_dict, keys)
        filter_dict = gen_filter_dict(query_dict, keys)
        filter_dict.update(parent_id=None)
        boards = Board.query.filter_by(
            **filter_dict).order_by(*order_by).paginate(page, number, True)
        data = {'title': 'Board', 'boards': boards}
        return render_template('board/board_list.html', **data)


class BoardView(MethodView):
    def get(self, boardId):
        board = Board.query.filter_by(id=boardId).first_or_404()
        has_children = board.children.exists()
        topics = self.topics(boardId, has_children)
        data = {'title': 'Board', 'board': board, 'topics': topics}
        return render_template('board/board.html', **data)

    def topics(self, boardId, has_children):
        query_dict = request.data
        page, number = self.page_info
        keys = ['title']
        order_by = gen_order_by(query_dict, keys)
        filter_dict = gen_filter_dict(query_dict, keys)
        if has_children:
            topics = Topic.query.outerjoin(Board).filter_by(**filter_dict).or_(
                Board.parent_id == boardId,
                Board.id == boardId).order_by(*order_by).paginate(page, number,
                                                                  True)
        else:
            filter_dict.update(board_id=boardId)
            topics = Topic.query.filter_by(
                **filter_dict).order_by(*order_by).paginate(page, number, True)
        return topics
