#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: permission.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-17 09:39:36 (CST)
# Last Update:星期六 2017-3-25 18:16:4 (CST)
#          By:
# Description:
# **************************************************************************
from .views import BaseView
from forums.extension import db
from forums.api.permission.models import Group, Router, Permission

__all__ = ['register_permission']


class GroupView(BaseView):
    column_editable_list = ['name']


class RouterView(BaseView):
    column_editable_list = ['url', 'url_type']
    column_formatters = dict(
        url_type=lambda v, c, m, p: m.get_choice_display('url_type', 'URL_TYPE')
    )
    form_choices = {'url_type': Router.URL_TYPE}


class PermissionView(BaseView):
    column_editable_list = ['allow', 'method']
    column_formatters = dict(
        allow=lambda v, c, m, p: m.get_choice_display('allow', 'PERMISSION'),
        method=lambda v, c, m, p: m.get_choice_display('method', 'METHOD'), )
    form_choices = {
        'allow': Permission.PERMISSION,
        'method': Permission.METHOD
    }


def register_permission(admin):
    admin.add_view(
        GroupView(
            Group,
            db.session,
            name='管理用户组',
            endpoint='admin_groups',
            category='管理权限'))
    admin.add_view(
        RouterView(
            Router,
            db.session,
            name='管理路由',
            endpoint='admin_routers',
            category='管理权限'))
    admin.add_view(
        PermissionView(
            Permission,
            db.session,
            name='管理权限',
            endpoint='admin_permiss',
            category='管理权限'))
