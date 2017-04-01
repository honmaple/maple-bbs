#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-04-01 18:34:38 (CST)
# Last Update:星期六 2017-4-1 20:6:3 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint
from .views import MessageListView

site = Blueprint('message', __name__, url_prefix='/message')

message_list = MessageListView.as_view('list')

site.add_url_rule('', view_func=message_list)
