#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: log.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-11-07 21:00:37 (CST)
# Last Update:星期日 2016-12-25 13:23:47 (CST)
#          By:
# Description:
# **************************************************************************
from api.user.urls import site as user_site
from api.permission.urls import site as perm_site
from api.topic.urls import site as topic_site
from api.reply.urls import site as reply_site
from api.tag.urls import site as tag_site
from api.board.urls import site as board_site
from api.auth.urls import site as auth_site
from api.forums.urls import site as forums_site
from api.mine.urls import site as mine_site
from api.follow.urls import site as follow_site
from api.setting.urls import site as setting_site
from api.upload.urls import site as upload_site
from docs.views import site as docs_site

# from maple.forums.urls import site as forums_site
# from docs.views import site as docs_site
# from api.urls import site as api_site
# from maple.auth.views import register_auth

# from flask_cors import CORS
# CORS(user_site)
# CORS(perm_site)
# CORS(topic_site)
# CORS(reply_site)
# CORS(auth_site)
# CORS(board_site)


def register_routes(app):
    app.register_blueprint(topic_site)
    app.register_blueprint(reply_site)
    app.register_blueprint(tag_site)
    app.register_blueprint(board_site)
    app.register_blueprint(user_site)
    app.register_blueprint(perm_site)
    app.register_blueprint(auth_site)
    app.register_blueprint(forums_site)
    app.register_blueprint(mine_site)
    app.register_blueprint(follow_site)
    app.register_blueprint(docs_site)
    app.register_blueprint(setting_site)
    app.register_blueprint(upload_site)
