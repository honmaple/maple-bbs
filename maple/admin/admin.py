#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: admin.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-31 21:42:11 (CST)
# Last Update:星期六 2016-11-12 21:13:0 (CST)
#          By:
# Description:
# **************************************************************************
from flask import abort
from flask_admin.contrib.sqla import ModelView
from flask_wtf import Form
from flask_principal import Permission, RoleNeed
from maple.forums.models import Board


class BaseForm(Form):
    def __init__(self, formdata=None, obj=None, prefix=u'', **kwargs):
        self._obj = obj
        super(BaseForm, self).__init__(
            formdata=formdata, obj=obj, prefix=prefix, **kwargs)


class BaseModelView(ModelView):

    page_size = 10
    can_view_details = True
    form_base_class = BaseForm

    def is_accessible(self):
        permission = Permission(RoleNeed('super'))
        return permission.can()

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


class PermissView(BaseModelView):
    column_display_pk = True
    column_list = ['id', 'name', 'roles', 'method', 'routes', 'is_allow']
    column_editable_list = ['is_allow', 'method']
    form_choices = {
        'method': [('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT'),
                   ('DELETE', 'DELETE')]
    }


class RoleView(BaseModelView):
    column_display_pk = True
    column_list = ['id', 'name', 'permissions', 'parents', 'children']


# def get_list():
#     endpoints = []
#     for rule in app.url_map.iter_rules():
#         endpoints.append((rule.endpoint, rule.endpoint))
#     return endpoints


class RouteView(BaseModelView):
    column_display_pk = True
    column_list = ['id', 'permissions', 'endpoint', 'rule']
    # form_choices = {'endpoint': get_list()}


class TagsModelView(BaseModelView):
    column_searchable_list = ['tagname']
    column_list = ['tagname', 'parents', 'children', 'summary', 'time']
    form_excluded_columns = ('tags', 'users', 'topics', 'followers')


class NoticeView(BaseModelView):
    column_filters = ['category', 'rece_user.username', 'send_user.username',
                      'is_read', 'publish']
    column_searchable_list = ['content']
    column_editable_list = ['is_read']
    form_widget_args = {'content': {'rows': 10}}
