#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-15 22:04:05 (CST)
# Last Update:星期六 2017-2-18 21:38:20 (CST)
#          By:
# Description:
# **************************************************************************
from flask import request, render_template
from common.views import BaseMethodView as MethodView
from .models import Board
from api.topic.models import Topic


class BoardListView(MethodView):
    def get(self):
        page, number = self.page_info
        boards = Board.get_list(page, number)
        data = {'title': 'Board', 'boards': boards}
        return render_template('board/board_list.html', **data)


class BoardView(MethodView):
    def get(self, boardId):
        board = Board.get(id=boardId)
        topics = self.topics(boardId)
        data = {'title': 'Board', 'board': board, 'topics': topics}
        return render_template('board/board.html', **data)

    def topics(self, boardId):
        page, number = self.page_info
        filter_dict = dict(board_id=boardId)
        topics = Topic.get_list(page, number, filter_dict)
        return topics
