#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-17 20:45:08 (CST)
# Last Update:星期六 2017-3-25 19:2:23 (CST)
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
        keys = ['name', 'description']
        order_by = gen_order_by(query_dict, keys)
        filter_dict = gen_filter_dict(query_dict, keys)
        boards = Board.query.filter_by(
            **filter_dict).order_by(*order_by).paginate(page, number, True)
        data = {'title': 'Board', 'boards': boards}
        return render_template('board/board_list.html', **data)


class BoardView(MethodView):
    def get(self, boardId):
        board = Board.query.filter_by(id=boardId).first_or_404()
        topics = self.topics(boardId)
        data = {'title': 'Board', 'board': board, 'topics': topics}
        return render_template('board/board.html', **data)

    def topics(self, boardId):
        page, number = self.page_info
        filter_dict = dict(board_id=boardId)
        topics = Topic.get_list(page, number, filter_dict)
        return topics
