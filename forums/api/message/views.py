#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-04-01 18:34:07 (CST)
# Last Update:星期六 2017-4-1 20:48:15 (CST)
#          By:
# Description:
# **************************************************************************
from flask import render_template, request

from forums.common.views import IsAuthMethodView as MethodView
from forums.count import Count

from .models import Message, MessageText


class MessageListView(MethodView):
    def get(self):
        query_dict = request.data
        user = request.user
        status = query_dict.pop('status', '0')
        page, number = self.page_info
        messages = Message.query.filter_by(
            receiver_id=user.id,
            status=status).order_by('-created_at').paginate(page, number, True)
        data = {'title': 'Notice', 'messages': messages}
        Count.user_message_count(user.id, clear=True)
        return render_template('forums/message.html', **data)
