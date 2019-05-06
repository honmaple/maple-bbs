#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-17 20:45:08 (CST)
# Last Update: Monday 2019-05-06 23:36:54 (CST)
#          By:
# Description:
# **************************************************************************
from flask import render_template, request
from flask_babel import gettext as _

from forums.api.topic.db import Topic
from forums.common.views import BaseMethodView as MethodView
from forums.common.utils import (gen_filter_dict, gen_order_by)
from forums.api.utils import gen_topic_filter, gen_topic_orderby

from .db import Board


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
        page, number = self.pageinfo
        keys = ['name']
        order_by = gen_order_by(query_dict, keys)
        filter_dict = gen_filter_dict(query_dict, keys)
        filter_dict.update(parent_id=None)
        boards = Board.query.filter_by(
            **filter_dict).order_by(*order_by).paginate(page, number, True)
        data = {'title': 'Board', 'boards': boards}
        return render_template('board/board_list.html', **data)


class BoardView(MethodView):
    def get(self, pk):
        board = Board.query.filter_by(id=pk).first_or_404()
        has_children = board.child_boards.exists()
        topics = self.topics(pk, has_children)
        data = {'title': 'Board', 'board': board, 'topics': topics}
        return render_template('board/board.html', **data)

    def topics(self, pk, has_children):
        query_dict = request.data
        page, number = self.pageinfo
        keys = ['title']
        # order_by = gen_order_by(query_dict, keys)
        # filter_dict = gen_filter_dict(query_dict, keys)
        order_by = gen_topic_orderby(query_dict, keys)
        filter_dict = gen_topic_filter(query_dict, keys)
        if has_children:
            o = []
            for i in order_by:
                if i.startswith('-'):
                    o.append(getattr(Topic, i.split('-')[1]).desc())
                else:
                    o.append(getattr(Topic, i))
            topics = Topic.query.filter_by(**filter_dict).outerjoin(Board).or_(
                Board.parent_id == pk,
                Board.id == pk).order_by(*o).paginate(page, number, True)
            return topics
        filter_dict.update(board_id=pk)
        topics = Topic.query.filter_by(
            **filter_dict).order_by(*order_by).paginate(page, number, True)
        return topics
