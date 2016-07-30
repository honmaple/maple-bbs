#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: users.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-07-02 20:12:26 (CST)
# Last Update:星期六 2016-7-30 13:44:11 (CST)
#          By:
# Description:
# **************************************************************************
from maple import db
from .admin import BaseModelView
from maple.user.models import User, UserInfor, UserSetting, Role
from wtforms import PasswordField
from wtforms.validators import DataRequired


class UserModelView(BaseModelView):
    column_exclude_list = ['password', 'infor', 'setting']
    column_searchable_list = ['username', 'email']
    column_filters = ['email', 'is_superuser', 'is_confirmed', 'register_time']
    column_editable_list = ['is_confirmed', 'is_superuser']
    column_details_exclude_list = ['infor', 'setting']
    form_columns = ('username', 'email', 'roles', 'is_confirmed')
    # inline_models = (UserInfor, UserSetting, Role)
    form_extra_fields = {'password': PasswordField('Password',
                                                   [DataRequired()])}


class UserInforModelView(BaseModelView):
    column_list = ['user', 'avatar', 'word', 'school', 'introduce']
    column_filters = ['user.username', 'school']
    column_searchable_list = ['school']
    # inline_models = [(User, dict(form_columns=['username']))]


class UserRoleModelView(BaseModelView):
    column_list = ['name', 'description', 'users']
    column_filters = ['users.username']
    column_searchable_list = ['name']


class UserSettingModelView(BaseModelView):
    column_list = ['user', 'online_status', 'topic_list', 'rep_list',
                   'ntb_list', 'collect_list', 'locale', 'timezone']
    column_sortable_list = (('user', 'user.username'), )


def admin_user(admin):
    admin.add_view(UserModelView(User,
                                 db.session,
                                 name='管理用户',
                                 endpoint='admin_users',
                                 url='user',
                                 category='管理用户'))
    admin.add_view(UserInforModelView(UserInfor,
                                      db.session,
                                      name='用户信息',
                                      endpoint='admin_user_info',
                                      category='管理用户'))
    admin.add_view(UserSettingModelView(UserSetting,
                                        db.session,
                                        name='用户设置',
                                        endpoint='admin_user_setting',
                                        category='管理用户'))
    admin.add_view(UserRoleModelView(Role,
                                     db.session,
                                     name='用户组',
                                     endpoint='admin_user_role',
                                     category='管理用户'))
