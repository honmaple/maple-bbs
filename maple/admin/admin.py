#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: admin.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-31 21:42:11 (CST)
# Last Update:星期六 2016-7-2 20:44:32 (CST)
#          By:
# Description:
# **************************************************************************
from maple import db, app
from maple.main.permission import super_permission
from maple.forums.models import Board, Count, Notice
from maple.topic.models import Tags
from flask import abort
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from flask_wtf import Form

admin = Admin(app, name='HonMaple', template_mode='bootstrap3')


class BaseModelView(ModelView):

    session = db.session
    page_size = 10
    can_view_details = True

    form_base_class = Form

    # form_base_class = SecureForm

    def is_accessible(self):
        return super_permission.can()

    def inaccessible_callback(self, name, **kwargs):
        abort(404)


class BoardModelView(BaseModelView):
    column_list = ['parent_board', 'board', 'description', 'rank',
                   'count.topics', 'count.all_topics']
    column_labels = {'count.topics': '主题', 'count.all_topics': '所有主题'}
    form_excluded_columns = ('topics')


class CountModelView(BaseModelView):
    column_list = ['board', 'topics', 'all_topics', 'drafts', 'collects',
                   'inviteds', 'follows']
    inline_models = [(Board, dict(form_excluded_columns=['topics']))]


class TagsModelView(BaseModelView):
    column_searchable_list = ['tagname']
    form_excluded_columns = ('users', 'topics', 'followers')


class NoticeView(BaseModelView):
    column_filters = ['category', 'rece_user.username', 'send_user.username',
                      'is_read', 'publish']
    column_searchable_list = ['content']
    column_editable_list = ['is_read']
    form_widget_args = {'content': {'rows': 10}}


admin.add_view(BoardModelView(Board,
                              db.session,
                              name='管理版块',
                              endpoint='admin_boards',
                              category='管理论坛'))
admin.add_view(CountModelView(Count,
                              db.session,
                              name='管理统计',
                              endpoint='admin_counts',
                              category='管理论坛'))
admin.add_view(TagsModelView(Tags,
                             db.session,
                             name='管理节点',
                             endpoint='admin_tags',
                             category='管理论坛'))
admin.add_view(NoticeView(
    Notice, db.session,
    name='管理通知', endpoint='admin_notice'))

from .admin_user import admin_user
from .admin_topic import admin_topic
from .admin_follow import admin_follow
# from .admin_file import admin_file
admin_user(admin)
admin_topic(admin)
admin_follow(admin)
# admin_file(admin)
