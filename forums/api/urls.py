#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-01-25 20:12:58 (CST)
# Last Update:星期二 2017-3-28 17:40:36 (CST)
#          By:
# Description:
# **************************************************************************
from .forums.urls import site as forums_site
from .auth.urls import site as auth_site
from .topic.urls import site as topic_site
from .tag.urls import site as tag_site
from .user.urls import site as user_site
from .setting.urls import site as setting_site
from .follow.urls import site as follow_site
from .upload.urls import site as upload_site
from .collect.urls import site as collect_site
# from .permission.urls import site as perm_site
# from .mine.urls import site as mine_site


def api_routers(app):
    app.register_blueprint(forums_site)
    app.register_blueprint(auth_site)
    app.register_blueprint(topic_site)
    app.register_blueprint(tag_site)
    app.register_blueprint(user_site)
    app.register_blueprint(setting_site)
    app.register_blueprint(follow_site)
    app.register_blueprint(upload_site)
    app.register_blueprint(collect_site)
    # app.register_blueprint(perm_site)
    # app.register_blueprint(mine_site)
