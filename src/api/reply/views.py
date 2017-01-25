#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-15 22:06:39 (CST)
# Last Update:星期三 2017-1-25 20:25:9 (CST)
#          By:
# Description:
# **************************************************************************
from flask import request, render_template, g, redirect
from flask.views import MethodView
from flask_maple.serializer import FlaskSerializer as Serializer
from flask_maple.response import HTTPResponse
from flask_maple.auth.forms import form_validate
from flask_login import current_user
from common.views import ViewListMixin
from .models import Reply
from .forms import ReplyForm


def error_callback():
    return redirect('/')


class ReplyListView(MethodView, ViewListMixin):
    def get(self):
        form = ReplyForm()
        page, number = self.page_info
        replies = Reply.get_list(page, number)
        if g.user.is_authenticated:
            like = Reply.query.filter_by(
                likers__username=current_user.username)
        data = {'replies': replies, 'form': form}
        return render_template('reply/reply_list.html', **data)
        # serializer = Serializer(replies, many=True)
        # return HTTPResponse(HTTPResponse.NORMAL_STATUS,
        #                     **serializer.data).to_response()

    @form_validate(ReplyForm, error=error_callback, f='')
    def post(self):
        post_data = request.data
        content = post_data.pop('content', None)
        topic = post_data.pop('topic', None)
        reply = Reply(content=content, topic_id=int(topic))
        reply.author = current_user
        reply.save()
        serializer = Serializer(reply, many=False)
        return HTTPResponse(HTTPResponse.NORMAL_STATUS,
                            **serializer.data).to_response()


class ReplyView(MethodView):
    def get(self, replyId):
        user = Reply.get(id=replyId)
        serializer = Serializer(user, many=False)
        return HTTPResponse(
            HTTPResponse.NORMAL_STATUS, data=serializer.data).to_response()

    def put(self, replyId):
        post_data = request.data
        reply = Reply.query.filter_by(id=replyId).first()
        content = post_data.pop('content', None)
        if content is not None:
            reply.content = content
        reply.save()
        serializer = Serializer(reply, many=False)
        return HTTPResponse(HTTPResponse.NORMAL_STATUS,
                            **serializer.data).to_response()

    def delete(self, replyId):
        reply = Reply.query.filter_by(id=replyId).first()
        reply.delete()
        serializer = Serializer(reply, many=False)
        return HTTPResponse(HTTPResponse.NORMAL_STATUS,
                            **serializer.data).to_response()


class LikeView(MethodView):
    def post(self, replyId):
        reply = Reply.query.filter_by(id=replyId).first()
        reply.likers.append(current_user)
        reply.save()
        serializer = Serializer(reply, many=False)
        return HTTPResponse(HTTPResponse.NORMAL_STATUS,
                            **serializer.data).to_response()

    def delete(self, replyId):
        reply = Reply.query.filter_by(id=replyId).first()
        reply.likers.remove(current_user)
        reply.save()
        serializer = Serializer(reply, many=False)
        return HTTPResponse(HTTPResponse.NORMAL_STATUS,
                            **serializer.data).to_response()
