#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-15 22:24:23 (CST)
# Last Update:星期六 2017-3-25 20:52:36 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint

from .views import (UserCollectListView, UserFollowingListView,
                    UserFollowerListView, UserListView, UserReplyListView,
                    UserView)

site = Blueprint('user', __name__, url_prefix='/user')

user_list = UserListView.as_view('list')
user = UserView.as_view('user')
topics = UserView.as_view('topic')
replies = UserReplyListView.as_view('reply')
collects = UserCollectListView.as_view('collect')
followers = UserFollowerListView.as_view('follower')
followings = UserFollowingListView.as_view('following')

site.add_url_rule('', view_func=user_list)
site.add_url_rule('/<username>', view_func=user)
site.add_url_rule('/<username>', view_func=topics)
site.add_url_rule('/<username>/topics', view_func=user)
site.add_url_rule('/<username>/replies', view_func=replies)
site.add_url_rule('/<username>/collects', view_func=collects)
site.add_url_rule('/<username>/followers', view_func=followers)
site.add_url_rule('/<username>/followings', view_func=followings)
