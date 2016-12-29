#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-15 22:22:44 (CST)
# Last Update:星期日 2016-12-18 16:37:59 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint
from .views import ReplyListView, ReplyView, LikeView

site = Blueprint('reply', __name__, url_prefix='/replies')

reply_list = ReplyListView.as_view('list')
reply = ReplyView.as_view('reply')
like_view = LikeView.as_view('like')

site.add_url_rule('', view_func=reply_list)
site.add_url_rule('/', view_func=reply_list)
site.add_url_rule('/<int:replyId>', view_func=reply)
site.add_url_rule('/<int:replyId>/like', view_func=like_view)
