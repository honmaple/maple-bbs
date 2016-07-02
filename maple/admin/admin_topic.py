#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: topics.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-07-02 20:15:46 (CST)
# Last Update:星期六 2016-7-2 20:17:44 (CST)
#          By:
# Description:
# **************************************************************************
from maple import db
from maple.topic.models import Topic, Reply
from maple.filters import Filters
from .admin import BaseModelView


class TopicModelView(BaseModelView):
    can_create = False
    column_searchable_list = ('title', 'content', 'author.username')
    column_filters = ['publish', 'is_good', 'is_top', 'author.username',
                      'vote']
    column_exclude_list = ['uid', 'content']
    column_editable_list = ['title', 'is_good', 'is_top']
    column_default_sort = 'publish'
    column_formatters = dict(
        content=lambda v, c, m, p: Filters.safe_markdown(m.content))
    form_widget_args = {'content': {'rows': 10}}
    form_excluded_columns = ('replies', 'collectors', 'followers', 'collects')

    form_ajax_refs = {'tags': {'fields': ('tagname', ), 'page_size': 10}}


class ReplyModelView(BaseModelView):
    column_searchable_list = ['topic.title', 'content']
    column_filters = ['author.username', 'publish', 'updated']
    form_excluded_columns = ['topic', 'likers']
    form_widget_args = {'content': {'rows': 10}}


class ReplyLikeView(BaseModelView):
    column_list = ['content', 'author', 'likers']
    form_columns = column_list


def admin_topic(admin):
    admin.add_view(TopicModelView(Topic,
                                  db.session,
                                  name='管理主题',
                                  endpoint='admin_topics',
                                  category='主题回复'))
    admin.add_view(ReplyModelView(Reply,
                                  db.session,
                                  name='管理回复',
                                  endpoint='admin_replies',
                                  category='主题回复'))
    admin.add_view(ReplyLikeView(Reply,
                                 db.session,
                                 name='回复点赞',
                                 endpoint='admin_reply_like',
                                 category='主题回复'))
