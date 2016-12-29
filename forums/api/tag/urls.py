#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-15 22:20:55 (CST)
# Last Update:星期六 2016-12-17 23:9:54 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint
from .views import TagsListView, TagsView, TagFeedView

site = Blueprint('tag', __name__, url_prefix='/tags')

tag_list = TagsListView.as_view('list')
tag = TagsView.as_view('tag')
tag_feed = TagFeedView.as_view('feed')

site.add_url_rule('', view_func=tag_list)
site.add_url_rule('/', view_func=tag_list)
site.add_url_rule('/<name>', view_func=tag)
site.add_url_rule('/<name>/feed', view_func=tag_feed)
