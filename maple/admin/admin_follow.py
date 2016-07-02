#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: follows.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-07-02 20:18:14 (CST)
# Last Update:星期六 2016-7-2 20:19:36 (CST)
#          By:
# Description:
# **************************************************************************
from maple import db, app
from maple.forums.models import Board, Count, Notice
from maple.user.models import User, UserInfor, UserSetting, Role
from maple.topic.models import Topic, Tags, Reply, Collect
from .admin import BaseModelView


class FollowView(BaseModelView):
    can_create = False
    column_searchable_list = ['username']
    column_filters = ['following_tags.tagname', 'following_topics.title',
                      'following_collects.name']
    column_list = ['username', 'following_tags', 'following_topics',
                   'following_collects', 'following_users']
    form_columns = ['following_tags', 'following_topics', 'following_collects',
                    'following_users']


class FollowTagsView(BaseModelView):
    can_create = False
    column_list = ['tagname', 'followers.username']
    column_filters = ['followers.username']
    column_searchable_list = ['tagname', 'followers.username']
    form_columns = ['tagname', 'followers']


class FollowTopicView(BaseModelView):
    can_create = False
    column_list = ['title', 'followers.username']
    column_filters = ['followers.username']
    column_searchable_list = column_list
    form_columns = ['title', 'followers']


class FollowCollectView(BaseModelView):
    can_create = False
    column_list = ['name', 'followers.username']
    column_filters = ['followers.username']
    column_searchable_list = column_list
    form_columns = ['name', 'followers']


class FollowUserView(BaseModelView):
    can_create = False
    column_list = ['username', 'followers.username']
    column_filters = ['followers.username']
    column_searchable_list = column_list
    # column_labels = {'username': '关注者', 'followers': '被关注者'}
    form_columns = ['username', 'followers']


def admin_follow(admin):
    admin.add_view(FollowView(User,
                              db.session,
                              name='全部关注',
                              endpoint='admin_follow',
                              category='管理关注'))
    admin.add_view(FollowTagsView(Tags,
                                  db.session,
                                  name='关注节点',
                                  endpoint='admin_follow_tags',
                                  category='管理关注'))
    admin.add_view(FollowTopicView(Topic,
                                   db.session,
                                   name='关注问题',
                                   endpoint='admin_follow_topic',
                                   category='管理关注'))
    admin.add_view(FollowCollectView(Collect,
                                     db.session,
                                     name='关注收藏',
                                     endpoint='admin_follow_collect',
                                     category='管理关注'))
    admin.add_view(FollowUserView(User,
                                  db.session,
                                  name='关注用户',
                                  endpoint='admin_follow_user',
                                  category='管理关注'))
