#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-22 21:49:08 (CST)
# Last Update:星期四 2017-3-30 15:26:49 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint
from .views import (FollowingTagsView, FollowingUsersView, FollowingTopicsView,
                    FollowingCollectsView)

site = Blueprint('follow', __name__, url_prefix='/following')

topic_view = FollowingTopicsView.as_view('topic')
tag_view = FollowingTagsView.as_view('tag')
user_view = FollowingUsersView.as_view('user')
collect_view = FollowingCollectsView.as_view('collect')

site.add_url_rule('', view_func=topic_view)
site.add_url_rule('/topics', view_func=topic_view)
site.add_url_rule('/tags', view_func=tag_view)
site.add_url_rule('/collects', view_func=collect_view)
site.add_url_rule('/users', view_func=user_view)
