#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: permissions.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-03-29 15:53:37 (CST)
# Last Update:星期四 2017-3-30 16:17:48 (CST)
#          By:
# Description:
# **************************************************************************
from flask import request
from flask_login import login_required

from forums.permission import (ReplyPermission, RestfulView, TopicPermission,
                               is_confirmed)


class Edit(RestfulView):
    def get(self, pk):
        permission = TopicPermission(pk)
        if not permission.can():
            return self.callback()
        return True


class TopicList(RestfulView):
    @is_confirmed
    def post(self):
        return True


class Topic(RestfulView):
    @is_confirmed
    def put(self, pk):
        permission = TopicPermission(pk)
        if not permission.can():
            return self.callback()
        return True

    @is_confirmed
    def delete(self, pk):
        permission = TopicPermission(pk)
        if not permission.can():
            return self.callback()
        return True


class ReplyList(RestfulView):
    @is_confirmed
    def post(self, pk):
        return True


class Reply(RestfulView):
    @is_confirmed
    def put(self, pk):
        return True

    @is_confirmed
    def delete(self, pk):
        return True


class Like(RestfulView):
    @is_confirmed
    def post(self, pk):
        return True

    @is_confirmed
    def delete(self, pk):
        return True


topic_list_permission = TopicList()
topic_permission = Topic()
reply_list_permission = ReplyList()
reply_permission = Reply()
like_permission = Like()
edit_permission = Edit()
