#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-17 09:36:57 (CST)
# Last Update:星期六 2016-12-17 9:39:16 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint
from .views import GroupListView, GroupView

site = Blueprint('perm', __name__)

group_list = GroupListView.as_view('list')
group = GroupView.as_view('group')

site.add_url_rule('/group', view_func=group_list)
site.add_url_rule('/group/<name>', view_func=group)
