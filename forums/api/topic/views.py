#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-15 22:07:39 (CST)
# Last Update: Thursday 2018-07-26 11:36:27 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Markup, redirect, render_template, request, url_for
from flask_babel import gettext as _
from flask_login import current_user, login_required

from flask_maple.form import form_validate
from flask_maple.response import HTTPResponse
from forums.api.forms import (CollectForm, ReplyForm, TopicForm,
                              collect_error_callback, error_callback,
                              form_board)
from forums.api.forums.models import Board
from forums.api.tag.models import Tags
from forums.api.utils import gen_topic_filter, gen_topic_orderby
from flask_maple.serializer import Serializer
from forums.common.utils import gen_filter_dict, gen_order_by
from forums.common.views import BaseMethodView as MethodView
from forums.common.views import IsAuthMethodView, IsConfirmedMethodView

from .models import Reply, Topic
from .permissions import (like_permission, reply_list_permission,
                          reply_permission, topic_list_permission,
                          topic_permission, edit_permission)
from forums.api.message.models import MessageClient


class TopicAskView(IsConfirmedMethodView):
    def get(self):
        boardId = request.args.get('boardId', type=int)
        form = form_board()
        if boardId is not None:
            form.category.data = boardId
        data = {'title': _('Ask - '), 'form': form}
        return render_template('topic/ask.html', **data)


class TopicEditView(IsConfirmedMethodView):
    decorators = (edit_permission, )

    def get(self, topicId):
        topic = Topic.query.filter_by(id=topicId).first_or_404()
        form = form_board()
        form.title.data = topic.title
        form.category.data = topic.board_id
        form.tags.data = ','.join([tag.name for tag in topic.tags])
        form.content.data = topic.content
        data = {'title': _('Edit -'), 'form': form, 'topic': topic}
        return render_template('topic/edit.html', **data)


class TopicListView(MethodView):
    decorators = (topic_list_permission, )

    def get(self):
        query_dict = request.data
        page, number = self.pageinfo
        keys = ['title']
        # order_by = gen_order_by(query_dict, keys)
        # filter_dict = gen_filter_dict(query_dict, keys)
        order_by = gen_topic_orderby(query_dict, keys)
        filter_dict = gen_topic_filter(query_dict, keys)
        title = _('All Topics')
        if request.path.endswith('good'):
            filter_dict.update(is_good=True)
            title = _('Good Topics')
        elif request.path.endswith('top'):
            filter_dict.update(is_top=True)
            title = _('Top Topics')
        topics = Topic.query.filter_by(
            **filter_dict).order_by(*order_by).paginate(page, number, True)
        data = {'title': title, 'topics': topics}
        return render_template('topic/topic_list.html', **data)

    @form_validate(form_board, error=error_callback, f='')
    def post(self):
        user = request.user
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
            tag = tag.strip()
            topic_tag = Tags.query.filter_by(name=tag).first()
            if topic_tag is None:
                topic_tag = Tags(name=tag, description=tag)
                topic_tag.save()
            topic_tags.append(topic_tag)
        topic.tags = topic_tags
        topic.author = user
        topic.save()
        # count
        topic.board.topic_count = 1
        topic.board.post_count = 1
        topic.author.topic_count = 1
        topic.reply_count = 1
        return redirect(url_for('topic.topic', topicId=topic.id))


class TopicView(MethodView):
    decorators = (topic_permission, )

    def get(self, topicId):
        form = ReplyForm()
        query_dict = request.data
        topic = Topic.query.filter_by(id=topicId).first_or_404()
        page, number = self.pageinfo
        keys = ['title']
        order_by = gen_order_by(query_dict, keys)
        filter_dict = gen_filter_dict(query_dict, keys)
        replies = topic.replies.filter_by(
            **filter_dict).order_by(*order_by).paginate(page, number, True)
        data = {
            'title': topic.title,
            'form': form,
            'topic': topic,
            'replies': replies
        }
        topic.read_count = 1
        return render_template('topic/topic.html', **data)

    @form_validate(form_board)
    def put(self, topicId):
        form = form_board()
        post_data = form.data
        topic = Topic.query.filter_by(id=topicId).first_or_404()
        title = post_data.pop('title', None)
        content = post_data.pop('content', None)
        content_type = post_data.pop('content_type', None)
        category = post_data.pop('category', None)
        if title is not None:
            topic.title = title
        if content is not None:
            topic.content = content
        if content_type is not None:
            topic.content_type = content_type
        if category is not None:
            topic.board_id = int(category)
        topic.save()
        return HTTPResponse(HTTPResponse.NORMAL_STATUS).to_response()


class ReplyListView(MethodView):
    decorators = (reply_list_permission, )

    @form_validate(ReplyForm, error=error_callback, f='')
    def post(self, topicId):
        topic = Topic.query.filter_by(id=topicId).first_or_404()
        post_data = request.data
        user = request.user
        content = post_data.pop('content', None)
        reply = Reply(content=content, topic_id=topic.id)
        reply.author = user
        reply.save()
        # notice
        MessageClient.topic(reply)
        # count
        topic.board.post_count = 1
        reply.author.reply_count = 1
        return redirect(url_for('topic.topic', topicId=topic.id))


class ReplyView(MethodView):

    decorators = (reply_permission, )

    def put(self, replyId):
        post_data = request.data
        reply = Reply.query.filter_by(id=replyId).first_or_404()
        content = post_data.pop('content', None)
        if content is not None:
            reply.content = content
        reply.save()
        return HTTPResponse(HTTPResponse.NORMAL_STATUS).to_response()

    def delete(self, replyId):
        reply = Reply.query.filter_by(id=replyId).first_or_404()
        reply.delete()
        return HTTPResponse(HTTPResponse.NORMAL_STATUS).to_response()


class LikeView(MethodView):

    decorators = (like_permission, )

    def post(self, replyId):
        user = request.user
        reply = Reply.query.filter_by(id=replyId).first_or_404()
        reply.likers.append(user)
        reply.save()
        MessageClient.like(reply)
        serializer = Serializer(reply, many=False)
        return HTTPResponse(
            HTTPResponse.NORMAL_STATUS, data=serializer.data).to_response()

    def delete(self, replyId):
        user = request.user
        reply = Reply.query.filter_by(id=replyId).first_or_404()
        reply.likers.remove(user)
        reply.save()
        serializer = Serializer(reply, many=False)
        return HTTPResponse(
            HTTPResponse.NORMAL_STATUS, data=serializer.data).to_response()
