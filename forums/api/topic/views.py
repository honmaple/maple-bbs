#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-15 22:07:39 (CST)
# Last Update:星期日 2016-12-18 19:59:28 (CST)
#          By:
# Description:
# **************************************************************************
from flask import request, render_template, redirect, url_for
from flask.views import MethodView
from flask_maple.serializer import FlaskSerializer as Serializer
from flask_maple.response import HTTPResponse
from flask_maple.auth.forms import form_validate
from flask_login import current_user
from flask_babelex import gettext as _
from api.board.models import Board
from api.tag.models import Tags
from api.common.views import ViewListMixin
from maple.helper import form_board
from .models import Topic, Collect
from .forms import TopicForm, ReplyForm, error_callback


class TopicAskView(MethodView):
    def get(self):
        boardId = request.args.get('boardId', type=int)
        form = form_board()
        if boardId is not None:
            form.category.data = boardId
        data = {'title': _('Ask - '), 'form': form}
        return render_template('topic/ask.html', **data)


class TopicEditView(MethodView):
    def get(self, topicId):
        topic = Topic.query.filter_by(uid=topicId).first_or_404()
        form = self.form()
        form.category.choices = [(b.id, b.board + '   --' + b.parent_board)
                                 for b in Board.query.all()]
        form.title.data = topic.title
        form.category.data = topic.board_id
        form.tags.data = ','.join([tag.tagname for tag in topic.tags])
        form.content.data = topic.content
        data = {'title': _('Edit -'), 'form': form, 'topic': topic}
        return render_template('topic/edit.html', **data)


class TopicPreviewView(MethodView):
    def post(self):
        choice = request.values.get('choice')
        content = request.values.get('content')
        return


class TopicListView(MethodView, ViewListMixin):
    @property
    def filter_dict(self):
        _dict = {}
        if request.path.endswith('good'):
            _dict.update(is_good=True)
        elif request.path.endswith('top'):
            _dict.update(is_top=True)
        return _dict

    def get(self):
        page, number = self.page_info
        filter_dict = self.filter_dict
        topics = Topic.get_list(page, number, filter_dict)
        return render_template('topic/topic_list.html', topics=topics)
        # serializer = Serializer(topics, many=True)
        # return HTTPResponse(HTTPResponse.NORMAL_STATUS,
        #                     **serializer.data).to_response()

    @form_validate(form_board, error=error_callback, f='')
    def post(self):
        form = form_board()
        post_data = form.data
        title = post_data.pop('title', None)
        content = post_data.pop('content', None)
        tags = post_data.pop('tags', None)
        content_type = post_data.pop('content_type', None)
        board = post_data.pop('category', None)
        topic = Topic(
            title=title,
            content=content,
            content_type=content_type,
            board_id=int(board))
        tags = tags.split(',')
        topic_tags = []
        for tag in tags:
            topic_tag = Tags.query.filter_by(name=tag).first()
            if topic_tag is None:
                topic_tag = Tags()
                topic_tag.name = tag
                topic_tag.description = tag
                topic_tag.save()
            topic_tags.append(topic_tag)
        topic.tags = topic_tags
        topic.author = current_user
        topic.save()
        return redirect(url_for('topic.topic', topicId=topic.id))
        # serializer = Serializer(topic, many=False)
        # return HTTPResponse(HTTPResponse.NORMAL_STATUS,
        #                     **serializer.data).to_response()


class TopicView(MethodView):
    def get(self, topicId):
        topic = Topic.get(id=topicId)
        return render_template('topic/topic.html', topic=topic)
        # serializer = Serializer(topic, many=False)
        # return HTTPResponse(
        #     HTTPResponse.NORMAL_STATUS, data=serializer.data).to_response()

    def put(self, topicId):
        post_data = request.data
        topic = Topic.query.filter_by(id=topicId).first()
        title = post_data.pop('title', None)
        content = post_data.pop('content', None)
        content_type = post_data.pop('content_type', None)
        board = post_data.pop('board', None)
        if title is not None:
            topic.title = title
        if content is not None:
            topic.content = content
        if content_type is not None:
            topic.content_type = content_type
        if board is not None:
            topic.board = int(board)
        topic.save()
        serializer = Serializer(topic, many=False)
        return HTTPResponse(HTTPResponse.NORMAL_STATUS,
                            **serializer.data).to_response()

    def delete(self, topicId):
        topic = Topic.query.filter_by(id=topicId).first()
        topic.delete()
        serializer = Serializer(topic, many=False)
        return HTTPResponse(HTTPResponse.NORMAL_STATUS,
                            **serializer.data).to_response()


class CollectListView(MethodView):
    def get(self):
        page, number = self.page_info
        collects = Collect.get_list(page, number)
        serializer = Serializer(collects, many=True)
        return HTTPResponse(HTTPResponse.NORMAL_STATUS,
                            **serializer.data).to_response()

    def post(self):
        post_data = request.data
        name = post_data.pop('name', None)
        description = post_data.pop('description', None)
        privacy = post_data.pop('privacy', None)
        collect = Collect(name=name, description=description, privacy=privacy)
        collect.author = current_user
        serializer = Serializer(collect, many=False)
        return HTTPResponse(HTTPResponse.NORMAL_STATUS,
                            **serializer.data).to_response()


class CollectView(MethodView):
    def get(self, collectId):
        collect = Collect.get(id=collectId)
        serializer = Serializer(collect, many=False)
        return HTTPResponse(
            HTTPResponse.NORMAL_STATUS, data=serializer.data).to_response()

    def put(self, collectId):
        post_data = request.data
        collect = Collect.query.filter_by(id=collectId).first()
        name = post_data.pop('name', None)
        description = post_data.pop('description', None)
        privacy = post_data.pop('privacy', None)
        if name is not None:
            collect.name = name
        if description is not None:
            collect.description = description
        if privacy is not None:
            collect.privacy = privacy
        collect.save()
        serializer = Serializer(collect, many=False)
        return HTTPResponse(HTTPResponse.NORMAL_STATUS,
                            **serializer.data).to_response()

    def delete(self, collectId):
        collect = Collect.query.filter_by(id=collectId).first()
        collect.delete()
        serializer = Serializer(collect, many=False)
        return HTTPResponse(HTTPResponse.NORMAL_STATUS,
                            **serializer.data).to_response()
