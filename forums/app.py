#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: app.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-03-28 16:11:07 (CST)
# Last Update:星期二 2017-9-19 12:49:24 (CST)
#          By:
# Description:
# **************************************************************************
from flask_principal import RoleNeed, UserNeed, identity_loaded
from flask_login import current_user
from .permission import TopicNeed, ReplyNeed, CollectNeed


def init_app(app):
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        '''基础权限'''
        identity.user = current_user

        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        if hasattr(current_user, 'is_superuser'):
            if current_user.is_superuser:
                identity.provides.add(RoleNeed('super'))

        if hasattr(current_user, 'is_confirmed'):
            if current_user.is_confirmed:
                identity.provides.add(RoleNeed('confirmed'))

        if hasattr(current_user, 'is_authenticated'):
            if current_user.is_authenticated:
                identity.provides.add(RoleNeed('auth'))
            else:
                identity.provides.add(RoleNeed('guest'))

        if hasattr(current_user, 'topics'):
            for topic in current_user.topics:
                identity.provides.add(TopicNeed(topic.id))

        if hasattr(current_user, 'replies'):
            for reply in current_user.replies:
                identity.provides.add(ReplyNeed(reply.id))

        if hasattr(current_user, 'collects'):
            for collect in current_user.collects:
                identity.provides.add(CollectNeed(collect.id))
