#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-03-28 16:15:16 (CST)
# Last Update:星期二 2017-3-28 21:27:14 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint
from .views import CollectListView, CollectView, AddToCollectView

site = Blueprint('collect', __name__)

site.add_url_rule('/collect', view_func=CollectListView.as_view('list'))
site.add_url_rule(
    '/collect/<int:pk>', view_func=CollectView.as_view('collect'))
site.add_url_rule(
    '/topic/<int:topicId>/collect',
    view_func=AddToCollectView.as_view('add_to_collect'))
