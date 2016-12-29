#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-15 22:04:05 (CST)
# Last Update:星期日 2016-12-18 0:18:5 (CST)
#          By:
# Description:
# **************************************************************************
from flask import request, render_template
from flask.views import MethodView
from flask_maple.serializer import FlaskSerializer as Serializer
from flask_maple.response import HTTPResponse
from api.common.views import ViewListMixin
from .models import Board


class BoardListView(MethodView, ViewListMixin):
    def get(self):
        page, number = self.page_info
        boards = Board.get_list(page, number)
        return render_template('board/board_list.html', boards=boards)
        # serializer = Serializer(boards, many=True)
        # return HTTPResponse(HTTPResponse.NORMAL_STATUS,
        #                     **serializer.data).to_response()

    def post(self):
        post_data = request.data
        name = post_data.pop('name', None)
        description = post_data.pop('description', None)
        parents = post_data.pop('parents', None)
        children = post_data.pop('children', None)
        board = Board(name=name, description=description)
        if parents is not None:
            parent_boards = Board.query.filter_by(id__in=parents)
            board.parents += parent_boards
        if children is not None:
            child_boards = Board.query.filter_by(id__in=children)
            board.children += child_boards
        board.save()
        serializer = Serializer(board, many=False)
        return HTTPResponse(HTTPResponse.NORMAL_STATUS,
                            **serializer.data).to_response()


class BoardView(MethodView):
    def get(self, boardId):
        board = Board.get(id=boardId)
        topics = board.topics.all()
        data = {'board': board, 'topics': topics}
        return render_template('board/board.html', **data)
        # serializer = Serializer(user, many=False)
        # return HTTPResponse(
        #     HTTPResponse.NORMAL_STATUS, data=serializer.data).to_response()

    def put(self, boardId):
        return 'put'

    def delete(self, boardId):
        return 'delete'
