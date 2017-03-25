#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: topic.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-17 13:01:43 (CST)
# Last Update:星期六 2017-3-25 19:37:7 (CST)
#          By:
# Description:
# **************************************************************************
from .views import BaseView
from forums.extension import db
from forums.api.topic.models import Topic, Collect, Reply
from forums.api.tag.models import Tags


class TopicView(BaseView):
    pass


class CollectView(BaseView):
    pass


class ReplyView(BaseView):
    pass


class TagView(BaseView):
    pass


def register_topic(admin):
    admin.add_view(
        TopicView(
            Topic,
            db.session,
            name='管理问题',
            endpoint='admin_topic',
            category='管理主题'))
    admin.add_view(
        CollectView(
            Collect,
            db.session,
            name='管理收藏',
            endpoint='admin_collect',
            category='管理主题'))
    admin.add_view(
        ReplyView(
            Reply,
            db.session,
            name='管理回复',
            endpoint='admin_reply',
            category='管理主题'))
    admin.add_view(
        TagView(
            Tags,
            db.session,
            name='管理节点',
            endpoint='admin_tags',
            category='管理主题'))
