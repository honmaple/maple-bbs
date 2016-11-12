#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-07-15 18:48:57 (CST)
# Last Update:星期日 2016-11-13 0:2:3 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint
from flask_login import login_required
from .views import (IndexView, ForumsView, NoticeView, UserListView, AboutView,
                    HelpView, ContactView, MessageView, OrderView)

site = Blueprint('forums', __name__)

index_view = IndexView.as_view('index')
forums_view = ForumsView.as_view('forums')
notice_view = NoticeView.as_view('notice')
userlist_view = UserListView.as_view('userlist')
about_view = AboutView.as_view('about')
help_view = HelpView.as_view('help')
contact_view = ContactView.as_view('contact')
message_view = MessageView.as_view('message')
order_view = OrderView.as_view('order')

site.add_url_rule('/', view_func=index_view)
site.add_url_rule('/index', view_func=forums_view)
site.add_url_rule('/notices', view_func=notice_view)
site.add_url_rule('/userlist', view_func=userlist_view)
site.add_url_rule('/about', view_func=about_view)
site.add_url_rule('/help', view_func=help_view)
site.add_url_rule('/contact', view_func=contact_view)
site.add_url_rule('/order', view_func=order_view)
site.add_url_rule('/messages/<receId>', view_func=message_view)
