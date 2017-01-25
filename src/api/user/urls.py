#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-15 22:24:23 (CST)
# Last Update:星期四 2016-12-22 21:45:11 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint
from .views import UserListView, UserView

site = Blueprint('user', __name__, url_prefix='/user')

user_list = UserListView.as_view('list')
user = UserView.as_view('user')

site.add_url_rule('', view_func=user_list)
site.add_url_rule('/', view_func=user_list)
site.add_url_rule('/<username>', view_func=user)
