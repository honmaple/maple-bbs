#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-07-15 18:43:51 (CST)
# Last Update:星期一 2016-8-1 17:16:41 (CST)
#          By:
# Description:
# **************************************************************************
from maple.forums.urls import site as forums_site
from maple.topic.urls import site as topic_site
from maple.board.urls import site as board_site
from maple.user.urls import site as user_site
from maple.mine.urls import site as mine_site
from maple.setting.urls import site as setting_site
from maple.upload.urls import site as upload_site
from maple.tag.urls import site as tag_site
from maple.docs.views import site as docs_site


def register_urls(app):
    app.register_blueprint(forums_site)
    app.register_blueprint(board_site, url_prefix='/<parent_b>')
    app.register_blueprint(tag_site, url_prefix='/t')
    app.register_blueprint(topic_site, url_prefix='/topic')
    app.register_blueprint(mine_site, url_prefix='/user')
    app.register_blueprint(user_site, url_prefix='/u/<user_url>')
    app.register_blueprint(setting_site, url_prefix='/setting')
    app.register_blueprint(upload_site)
    app.register_blueprint(docs_site, subdomain='docs')
    from maple.auth import views
    from maple.admin import admin
