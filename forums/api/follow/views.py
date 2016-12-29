#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-22 21:49:05 (CST)
# Last Update:星期四 2016-12-22 22:23:39 (CST)
#          By:
# Description:
# **************************************************************************
from flask.views import MethodView
from flask import (render_template, request, redirect, url_for, jsonify,
                   current_app)
from flask_login import current_user
from api.common.views import ViewListMixin
from api.tag.models import Tags
from api.topic.models import Topic, Collect


class FollowingTagsView(MethodView, ViewListMixin):
    def get(self):
        page, number = self.page_info
        filter_dict = {'followers__username': current_user.username}
        tags = Tags.get_list(page, number, filter_dict)
        data = {'tags': tags}
        return render_template('follow/following_tags.html', **data)


class FollowingTopicsView(MethodView, ViewListMixin):
    def get(self):
        page, number = self.page_info
        filter_dict = {'followers__username': current_user.username}
        topics = Topic.get_list(page, number, filter_dict)
        data = {'topics': topics}
        return render_template('follow/following_topics.html', **data)


class FollowingUsersView(MethodView, ViewListMixin):
    def get(self):
        page, number = self.page_info
        users = current_user.following_users.paginate(page, number, True)
        data = {'users': users}
        return render_template('follow/following_users.html', **data)


class FollowingCollectsView(MethodView, ViewListMixin):
    def get(self):
        page, number = self.page_info
        filter_dict = {'followers__username': current_user.username}
        collects = Collect.get_list(page, number, filter_dict)
        data = {'collects': collects}
        return render_template('follow/following_collects.html', **data)
