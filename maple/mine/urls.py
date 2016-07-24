#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-07-15 19:19:41 (CST)
# Last Update:星期日 2016-7-24 16:53:43 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint
from flask_login import login_required
from maple.helpers import register_api
from .views import CollectAPI, LikeAPI, FollowAPI, CollectDetailAPI
from .views import collect_following

site = Blueprint('mine', __name__)
site.add_url_rule('/collect/following',
                  view_func=login_required(collect_following))

register_api(site, CollectAPI, 'collect', '/collect', 'collectId')
register_api(site, CollectDetailAPI, 'collect_detail', '/collect/detail',
             'collectId')

# register_api(FollowAPI, 'follow', '/follow', 'type', 'string')

follow_view = FollowAPI.as_view('follow')
site.add_url_rule('/follow',
                  defaults={'type': 'topic'},
                  view_func=follow_view,
                  methods=['GET'])
site.add_url_rule('/follow/<type>',
                  view_func=follow_view,
                  methods=['GET', 'POST', 'DELETE'])

like_view = LikeAPI.as_view('like')
site.add_url_rule('/like/<int:replyId>',
                  view_func=like_view,
                  methods=['POST', 'DELETE'])
