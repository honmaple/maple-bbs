#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-07-15 19:19:41 (CST)
# Last Update:星期五 2016-7-15 19:22:40 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint
from .views import CollectAPI,LikeAPI,FollowAPI
from .views import collect_following, add_collect, delete_collect

site = Blueprint('mine', __name__)
site.add_url_rule('/collect/following', view_func=collect_following)
site.add_url_rule('/add-to-collect', view_func=add_collect, methods=['POST'])
site.add_url_rule('/delete-from-collect',
                  view_func=delete_collect,
                  methods=['DELETE'])

def register_api(view, endpoint, url):
    view_func = view.as_view(endpoint)
    site.add_url_rule(url,
                      defaults={'uid': None},
                      view_func=view_func,
                      methods=['GET', 'POST', 'DELETE'])


def register_draft(view, endpoint, url):
    view_func = view.as_view(endpoint)
    site.add_url_rule(url,
                      defaults={'uid': None},
                      view_func=view_func,
                      methods=['GET', 'POST'])
    site.add_url_rule('%s/<int:uid>' % url,
                      view_func=view_func,
                      methods=['GET', 'PUT', 'DELETE'])


collect_view = CollectAPI.as_view('collect')
site.add_url_rule('/collect',
                  defaults={'uid': None},
                  view_func=collect_view,
                  methods=['GET', ])
site.add_url_rule('/collect', view_func=collect_view, methods=['POST', ])
site.add_url_rule('/collect/<uid>',
                  view_func=collect_view,
                  methods=['GET', 'PUT', 'DELETE'])

follow_view = FollowAPI.as_view('follow')
site.add_url_rule('/follow',
                  defaults={'type': 'topics'},
                  view_func=follow_view,
                  methods=['GET', ])
site.add_url_rule('/follow', view_func=follow_view, methods=['POST', 'DELETE'])
site.add_url_rule('/follow/<type>', view_func=follow_view, methods=['GET'])

like_view = LikeAPI.as_view('like')
site.add_url_rule('/like', view_func=like_view, methods=['POST', 'DELETE'])
