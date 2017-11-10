#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-04-01 18:34:38 (CST)
# Last Update:星期五 2017-11-10 10:57:22 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint
from .views import MessageListView

site = Blueprint('message', __name__, url_prefix='/message')

message_list = MessageListView.as_view('list')

site.add_url_rule('', view_func=message_list)


def init_app(app):
    app.register_blueprint(site)
