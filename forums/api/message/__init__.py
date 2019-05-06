#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: __init__.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-04-01 18:33:33 (CST)
# Last Update: Monday 2019-05-06 23:00:30 (CST)
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
