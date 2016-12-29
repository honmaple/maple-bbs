#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-15 22:15:34 (CST)
# Last Update:星期日 2016-12-18 18:48:31 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint
from .views import (TopicAskView, TopicEditView, TopicPreviewView,
                    TopicListView, TopicView, CollectListView, CollectView)

site = Blueprint('topic', __name__)

topic_list = TopicListView.as_view('list')
topic_good_list = TopicListView.as_view('good')
topic_top_list = TopicListView.as_view('top')
topic = TopicView.as_view('topic')
ask_view = TopicAskView.as_view('ask')
edit_view = TopicEditView.as_view('edit')
preview_view = TopicPreviewView.as_view('preview')

collect_list = CollectListView.as_view('collectlist')
collect = CollectView.as_view('collect')


site.add_url_rule('/topic/ask', view_func=ask_view)
site.add_url_rule('/topic/preview', view_func=preview_view)
site.add_url_rule('/topic', view_func=topic_list)
site.add_url_rule('/topic/top', view_func=topic_top_list)
site.add_url_rule('/topic/good', view_func=topic_good_list)
site.add_url_rule('/topic/<int:topicId>', view_func=topic)
site.add_url_rule('/topic/<int:topicId>/edit', view_func=edit_view)

site.add_url_rule('/collect', view_func=collect_list)
site.add_url_rule('/collect/<int:collectId>', view_func=collect)
