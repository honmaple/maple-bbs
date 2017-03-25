#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-22 21:49:05 (CST)
# Last Update:星期六 2017-3-25 20:27:38 (CST)
#          By:
# Description:
# **************************************************************************
from flask import (request, render_template)
from forums.api.tag.models import Tags
from forums.api.topic.models import Collect, Topic
from forums.common.views import IsAuthMethodView as MethodView


class FollowingTagsView(MethodView):
    def get(self):
        user = request.user
        page, number = self.page_info
        filter_dict = {'followers__username': user.username}
        tags = Tags.query.filter_by(**filter_dict).paginate(page, number, True)
        data = {'tags': tags}
        return render_template('follow/following_tags.html', **data)


class FollowingTopicsView(MethodView):
    def get(self):
        user = request.user
        page, number = self.page_info
        filter_dict = {'followers__username': user.username}
        topics = Topic.query.filter_by(**filter_dict).paginate(page, number,
                                                               True)
        data = {'topics': topics}
        return render_template('follow/following_topics.html', **data)


class FollowingUsersView(MethodView):
    def get(self):
        user = request.user
        page, number = self.page_info
        users = user.following_users.paginate(page, number, True)
        data = {'users': users}
        return render_template('follow/following_users.html', **data)


class FollowingCollectsView(MethodView):
    def get(self):
        user = request.user
        page, number = self.page_info
        filter_dict = {'followers__username': user.username}
        collects = Collect.query.filter_by(**filter_dict).paginate(
            page, number, True)

        data = {'collects': collects}
        return render_template('follow/following_collects.html', **data)
