#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: app.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-11-12 20:39:15 (CST)
# Last Update:星期六 2016-11-12 21:8:38 (CST)
#          By:
# Description:
# **************************************************************************
from flask_principal import RoleNeed, UserNeed, identity_loaded
from flask_login import current_user
from maple.permission.permission import EditTopicNeed, GetCollect, PostCollect


def register_app(app):
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        '''基础权限'''
        identity.user = current_user

        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))

        if hasattr(current_user, 'is_superuser'):
            if current_user.is_superuser:
                identity.provides.add(RoleNeed('super'))

        if hasattr(current_user, 'topics'):
            for topic in current_user.topics:
                identity.provides.add(EditTopicNeed(topic.uid))

        if hasattr(current_user, 'collects'):
            for collect in current_user.collects:
                identity.provides.add(GetCollect(collect.id))
                identity.provides.add(PostCollect(collect.id))
