#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: follows.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-07-02 20:18:14 (CST)
# Last Update:星期日 2016-7-24 19:57:23 (CST)
#          By:
# Description:
# **************************************************************************
from maple import db
from maple.user.models import User
from .admin import BaseModelView


class FollowView(BaseModelView):
    can_create = False
    column_searchable_list = ['username']
    column_filters = ['username', 'following_tags.tagname',
                      'following_topics.title', 'following_collects.name',
                      'following_users.username']
    column_list = ['username', 'following_tags', 'following_topics',
                   'following_collects', 'following_users']
    form_columns = column_list


class FollowTagsView(BaseModelView):
    can_create = False
    column_list = ['username', 'following_tags']
    column_filters = ['username', 'following_tags.tagname']
    column_searchable_list = ['following_tags.tagname', 'username']
    form_columns = ['username', 'following_tags']


class FollowTopicView(BaseModelView):
    can_create = False
    column_list = ['username', 'following_topics']
    column_filters = ['username', 'following_topics.title']
    column_searchable_list = column_filters
    form_columns = ['username', 'following_topics']


class FollowCollectView(BaseModelView):
    can_create = False
    column_list = ['username', 'following_collects']
    column_filters = ['username', 'following_collects.name']
    column_searchable_list = column_filters
    form_columns = column_list
    # column_filters = ['followers.username']
    # column_searchable_list = column_list
    # form_columns = ['name', 'followers']


class FollowUserView(BaseModelView):
    can_create = False
    column_list = ['username', 'following_users']
    column_labels = {'username': '被关注者', 'following_users': '关注者'}
    column_filters = ['username', 'following_users.username']
    column_searchable_list = column_filters
    form_columns = column_list


def admin_follow(admin):
    admin.add_view(FollowView(User,
                              db.session,
                              name='全部关注',
                              endpoint='admin_follow',
                              category='管理关注'))
    admin.add_view(FollowTagsView(User,
                                  db.session,
                                  name='关注节点',
                                  endpoint='admin_follow_tags',
                                  category='管理关注'))
    admin.add_view(FollowTopicView(User,
                                   db.session,
                                   name='关注问题',
                                   endpoint='admin_follow_topic',
                                   category='管理关注'))
    admin.add_view(FollowCollectView(User,
                                     db.session,
                                     name='关注收藏',
                                     endpoint='admin_follow_collect',
                                     category='管理关注'))
    admin.add_view(FollowUserView(User,
                                  db.session,
                                  name='关注用户',
                                  endpoint='admin_follow_user',
                                  category='管理关注'))
