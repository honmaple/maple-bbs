#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: message.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-04-01 18:52:43 (CST)
# Last Update:星期五 2017-11-10 11:06:11 (CST)
#          By:
# Description:
# **************************************************************************
from .views import BaseView
from forums.extension import db
from forums.api.message.db import MessageText, Message


class MessageTextView(BaseView):
    pass


class MessageView(BaseView):
    pass
    # column_searchable_list = ['name']
    # form_excluded_columns = ('topics', 'followers')


def init_admin(admin):
    admin.add_view(
        MessageView(
            Message,
            db.session,
            name='管理通知',
            endpoint='admin_message',
            category='管理通知'))
    admin.add_view(
        MessageTextView(
            MessageText,
            db.session,
            name='管理内容',
            endpoint='admin_message_text',
            category='管理通知'))
