#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-21 22:18:28 (CST)
# Last Update:星期四 2016-12-22 21:47:12 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint, g, abort
from .views import (UserTopicListView, UserReplyListView, UserCollectListView,
                    UserFollowerListView, UserFollowingListView)
from api.user.models import User

site = Blueprint('mine', __name__, url_prefix='/u/<username>')


@site.url_value_preprocessor
def pull_user_url(endpoint, values):
    g.username = values.pop('username')
    user = User.query.filter_by(username=g.username).first()
    if user is None:
        abort(404)


@site.url_defaults
def add_user_url(endpoint, values):
    if 'username' in values or not g.username:
        return
    values['username'] = g.username


topic_list_view = UserTopicListView.as_view('topiclist')
reply_list_view = UserReplyListView.as_view('replylist')
collect_list_view = UserCollectListView.as_view('collectlist')
follower_list_view = UserFollowerListView.as_view('followerlist')
following_list_view = UserFollowingListView.as_view('followinglist')

site.add_url_rule('', view_func=topic_list_view)
site.add_url_rule('/topic', view_func=topic_list_view)
site.add_url_rule('/reply', view_func=reply_list_view)
site.add_url_rule('/collect', view_func=collect_list_view)
site.add_url_rule('/follower', view_func=follower_list_view)
site.add_url_rule('/following', view_func=following_list_view)
