#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-07-15 18:12:22 (CST)
# Last Update:星期日 2016-11-6 11:1:59 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint
from .views import (TopicAskView, TopicEditView, TopicPreviewView,
                    TopicGoodListView, TopicTopListView, TopicVoteView,
                    TopicListView, TopicView, ReplyListView)

site = Blueprint('topic', __name__)

ask_view = TopicAskView.as_view('ask')
edit_view = TopicEditView.as_view('edit')
preview_view = TopicPreviewView.as_view('preview')
good_view = TopicGoodListView.as_view('good')
top_view = TopicTopListView.as_view('top')
vote_view = TopicVoteView.as_view('vote')
topiclist_view = TopicListView.as_view('topiclist')
topic_view = TopicView.as_view('topic')
replylist_view = ReplyListView.as_view('reply')

site.add_url_rule('/ask', view_func=ask_view)
site.add_url_rule('/good', view_func=good_view)
site.add_url_rule('/top', view_func=top_view)
site.add_url_rule('/preview', view_func=preview_view)
site.add_url_rule('', view_func=topiclist_view)
site.add_url_rule('/<topicId>', view_func=topic_view)
site.add_url_rule('/<topicId>/edit', view_func=edit_view)
site.add_url_rule('/<topicId>/vote', view_func=vote_view)
site.add_url_rule('/<topicId>/reply', view_func=replylist_view)
