#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: permissions.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-03-29 15:53:37 (CST)
# Last Update:星期三 2017-3-29 18:38:9 (CST)
#          By:
# Description:
# **************************************************************************
from flask import request
from flask_login import login_required

from forums.permission import (ReplyPermission, RestfulView, TopicPermission,
                               is_confirmed)


class TopicList(RestfulView):
    @is_confirmed
    def post(self):
        return True


class Topic(RestfulView):
    @is_confirmed
    def put(self, topicId):
        permission = TopicPermission(topicId)
        if not permission.can():
            return self.callback()
        return True

    @is_confirmed
    def delete(self, topicId):
        permission = TopicPermission(topicId)
        if not permission.can():
            return self.callback()
        return True


class ReplyList(RestfulView):
    @is_confirmed
    def post(self, topicId):
        return True


class Reply(RestfulView):
    @is_confirmed
    def put(self, replyId):
        return True

    @is_confirmed
    def delete(self, replyId):
        return True


class Like(RestfulView):
    @is_confirmed
    def post(self, replyId):
        return True

    @is_confirmed
    def delete(self, replyId):
        return True


topic_list_permission = TopicList()
topic_permission = Topic()
reply_list_permission = ReplyList()
reply_permission = Reply()
like_permission = Like()
