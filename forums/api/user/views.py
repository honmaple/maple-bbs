#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-15 22:08:06 (CST)
# Last Update:星期六 2017-3-25 21:8:57 (CST)
#          By:
# Description:
# **************************************************************************
from flask import redirect, render_template, request, url_for
from flask_login import current_user
from forums.api.forums.models import Board
from forums.api.tag.models import Tags
from forums.api.topic.models import Topic, Reply, Collect
from forums.common.utils import gen_filter_dict, gen_order_by
from forums.common.views import BaseMethodView as MethodView

from .models import User


class UserListView(MethodView):
    def get(self):
        query_dict = request.data
        page, number = self.page_info
        keys = ['username']
        order_by = gen_order_by(query_dict, keys)
        filter_dict = gen_filter_dict(query_dict, keys)
        users = User.query.filter_by(
            **filter_dict).order_by(*order_by).paginate(page, number, True)
        return render_template('user/user_list.html', users=users)


class UserView(MethodView):
    def get(self, username):
        query_dict = request.data
        user = User.query.filter_by(username=username).first_or_404()
        page, number = self.page_info
        keys = ['title']
        order_by = gen_order_by(query_dict, keys)
        filter_dict = gen_filter_dict(query_dict, keys)
        filter_dict.update(author_id=user.id)
        topics = Topic.query.filter_by(
            **filter_dict).order_by(*order_by).paginate(page, number, True)
        setting = user.setting
        topic_is_allowed = False
        if setting.topic_list == 1 or (setting.topic_list == 2 and
                                       current_user.is_authenticated):
            topic_is_allowed = True
        data = {
            'topics': topics,
            'user': user,
            'topic_is_allowed': topic_is_allowed
        }
        return render_template('user/user.html', **data)


class UserReplyListView(MethodView):
    def get(self, username):
        query_dict = request.data
        user = User.query.filter_by(username=username).first_or_404()
        page, number = self.page_info
        keys = ['title']
        order_by = gen_order_by(query_dict, keys)
        filter_dict = gen_filter_dict(query_dict, keys)
        filter_dict.update(author_id=user.id)
        replies = Reply.query.filter_by(
            **filter_dict).order_by(*order_by).paginate(page, number, True)
        setting = user.setting
        replies_is_allowed = False
        if setting.rep_list == 1 or (current_user.is_authenticated and
                                     setting.rep_list == 2):
            replies_is_allowed = True
        data = {
            'replies': replies,
            'user': user,
            'replies_is_allowed': replies_is_allowed
        }
        return render_template('user/replies.html', **data)


class UserFollowerListView(MethodView):
    def get(self, username):
        query_dict = request.data
        user = User.query.filter_by(username=username).first_or_404()
        page, number = self.page_info
        keys = ['title']
        order_by = gen_order_by(query_dict, keys)
        filter_dict = gen_filter_dict(query_dict, keys)
        filter_dict.update(author_id=user.id)
        followers = Collect.query.filter_by(
            **filter_dict).order_by(*order_by).paginate(page, number, True)
        data = {'followers': followers, 'user': user}
        return render_template('user/followers.html', **data)


class UserFollowingListView(MethodView):
    def get(self):
        return redirect(url_for('follow.topic'))


class UserCollectListView(MethodView):
    def get(self, username):
        return redirect(url_for('follow.collect'))
