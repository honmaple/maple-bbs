#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: user.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-17 11:57:11 (CST)
# Last Update:星期五 2017-11-10 11:05:56 (CST)
#          By:
# Description:
# **************************************************************************
from .views import BaseView
from forums.extension import db
from forums.api.user.models import User, UserInfo, UserSetting
from wtforms import PasswordField
from wtforms.validators import DataRequired

STATUS = UserSetting.STATUS


def display_status(column):
    return lambda v, c, m, p: m.get_choice_display(column, 'STATUS')


class UserView(BaseView):
    column_exclude_list = ['password', 'info', 'setting']
    column_searchable_list = ['username', 'email']
    column_filters = ['email', 'is_superuser', 'is_confirmed', 'register_time']
    column_editable_list = ['is_confirmed', 'is_superuser']
    form_columns = ('username', 'email', 'password', 'is_confirmed',
                    'is_superuser')
    # inline_models = (UserInfo, UserSetting)
    # form_extra_fields = {
    #     'password': PasswordField('Password', [DataRequired()])
    # }


class UserInfoView(BaseView):
    pass


class UserSettingView(BaseView):
    column_formatters = dict(
        online_status=display_status('online_status'),
        topic_list=display_status('topic_list'),
        rep_list=display_status('rep_list'),
        ntb_list=display_status('ntb_list'),
        collect_list=display_status('collect_list'),
        locale=lambda v, c, m, p: m.get_choice_display('locale', 'LOCALE'),
        timezone=lambda v, c, m, p: m.get_choice_display('timezone', 'TIMEZONE'),
    )
    column_editable_list = column_formatters.keys()
    form_choices = {
        'online_status': UserSetting.STATUS,
        'topic_list': UserSetting.STATUS,
        'rep_list': UserSetting.STATUS,
        'ntb_list': UserSetting.STATUS,
        'collect_list': UserSetting.STATUS,
        'locale': UserSetting.LOCALE,
        'timezone': UserSetting.TIMEZONE
    }


def init_admin(admin):
    admin.add_view(
        UserView(
            User,
            db.session,
            name='管理用户',
            endpoint='admin_user',
            category='管理用户'))
    admin.add_view(
        UserInfoView(
            UserInfo,
            db.session,
            name='管理用户信息',
            endpoint='admin_userinfo',
            category='管理用户'))
    admin.add_view(
        UserSettingView(
            UserSetting,
            db.session,
            name='管理用户设置',
            endpoint='admin_usersetting',
            category='管理用户'))
