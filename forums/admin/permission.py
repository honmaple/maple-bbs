#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: permission.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-17 09:39:36 (CST)
# Last Update:星期一 2017-12-25 17:48:59 (CST)
#          By:
# Description:
# **************************************************************************
from .views import BaseView
from forums.extension import db
from forums.api.user.db import Group, Permission


class GroupView(BaseView):
    column_editable_list = ['name']


class PermissionView(BaseView):
    column_searchable_list = ('resource', 'groups.name')
    column_filters = ['groups.name', 'resource_type']
    column_editable_list = ['code']


def init_admin(admin):
    admin.add_view(
        GroupView(
            Group,
            db.session,
            name='管理用户组',
            endpoint='admin_groups',
            category='管理权限'))
    admin.add_view(
        PermissionView(
            Permission,
            db.session,
            name='管理权限',
            endpoint='admin_permiss',
            category='管理权限'))
