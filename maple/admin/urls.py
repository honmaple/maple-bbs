#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-11-12 20:42:58 (CST)
# Last Update:星期六 2016-11-12 21:13:7 (CST)
#          By:
# Description:
# **************************************************************************
from maple.forums.models import Board, Count, Notice
from maple.tag.models import Tags
from maple.user.models import Role
from maple.permission.models import Permiss, Route
from maple.extension import admin, db
from .admin import (BoardModelView, CountModelView, TagsModelView, RoleView,
                    PermissView, RouteView, NoticeView)

admin.add_view(
    BoardModelView(
        Board,
        db.session,
        name='管理版块',
        endpoint='admin_boards',
        category='管理论坛'))
admin.add_view(
    CountModelView(
        Count,
        db.session,
        name='管理统计',
        endpoint='admin_counts',
        category='管理论坛'))
admin.add_view(
    TagsModelView(
        Tags, db.session, name='管理节点', endpoint='admin_tags', category='管理论坛'))
admin.add_view(
    RoleView(
        Role,
        db.session,
        name='管理用户组',
        endpoint='admin_role_permission',
        category='权限管理'))
admin.add_view(
    PermissView(
        Permiss,
        db.session,
        name='管理权限',
        endpoint='admin_permiss',
        category='权限管理'))
admin.add_view(
    RouteView(
        Route,
        db.session,
        name='管理视图',
        endpoint='admin_route',
        category='权限管理'))
admin.add_view(
    NoticeView(
        Notice, db.session, name='管理通知', endpoint='admin_notice'))

from .admin_user import admin_user
from .admin_topic import admin_topic
from .admin_follow import admin_follow
# from .admin_file import admin_file
admin_user(admin)
admin_topic(admin)
admin_follow(admin)
# admin_file(admin)
