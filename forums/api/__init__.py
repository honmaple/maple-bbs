#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: __init__.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-11-20 15:49:33 (CST)
# Last Update:星期五 2018-01-05 00:21:42 (CST)
#          By:
# Description:
# **************************************************************************
from forums.api.forums import urls as forums_url
from forums.api.user import urls as user_url
from forums.api.tag import urls as tag_url
from forums.api.topic import urls as topic_url
from forums.api.collect import urls as collect_url
from forums.api.message import urls as message_url
from forums.api.setting import urls as setting_url
from forums.api.upload import urls as upload_url
from forums.api.follow import urls as follow_url
from forums.api.search import urls as search_url


def init_app(app):
    forums_url.init_app(app)
    user_url.init_app(app)
    tag_url.init_app(app)
    topic_url.init_app(app)
    collect_url.init_app(app)
    message_url.init_app(app)
    follow_url.init_app(app)
    setting_url.init_app(app)
    upload_url.init_app(app)
    search_url.init_app(app)
    # blueprints = [
    #     'forums.api.forums.urls'
    #     # 'forums.api.auth.urls',
    #     'forums.api.tag.urls',
    #     # 'forums.api.topic',
    #     # 'forums.api.user.urls',
    #     # 'forums.api.setting',
    #     # 'forums.api.follow',
    #     # 'forums.api.upload',
    #     # 'forums.api.collect',
    #     # 'forums.api.message',
    #     # 'forums.api.search'
    # ]
    # for blueprint in blueprints:
    #     import_module(blueprint).init_app(app)
    #     # app.register_blueprint(import_module(blueprint))
