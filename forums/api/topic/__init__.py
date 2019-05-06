#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: __init__.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-13 23:22:48 (CST)
# Last Update: Monday 2019-05-06 23:03:23 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint

site = Blueprint('topic', __name__)


def init_app(app):
    from .views import (LikeView, ReplyListView, ReplyView, TopicAskView,
                        TopicEditView, TopicListView, TopicView)
    topic_list = TopicListView.as_view('list')
    topic_good_list = TopicListView.as_view('good')
    topic_top_list = TopicListView.as_view('top')
    topic = TopicView.as_view('topic')
    ask_view = TopicAskView.as_view('ask')
    edit_view = TopicEditView.as_view('edit')

    reply_list = ReplyListView.as_view('reply_list')
    reply = ReplyView.as_view('reply')
    like_view = LikeView.as_view('reply_like')

    site.add_url_rule('/topic/ask', view_func=ask_view)
    site.add_url_rule('/topic', view_func=topic_list)
    site.add_url_rule('/topic/top', view_func=topic_top_list)
    site.add_url_rule('/topic/good', view_func=topic_good_list)
    site.add_url_rule('/topic/<int:topicId>', view_func=topic)
    site.add_url_rule('/topic/<int:topicId>/edit', view_func=edit_view)
    site.add_url_rule('/topic/<int:topicId>/replies', view_func=reply_list)
    site.add_url_rule('/replies/<int:replyId>', view_func=reply)
    site.add_url_rule('/replies/<int:replyId>/like', view_func=like_view)
    app.register_blueprint(site)
