#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-21 21:56:49 (CST)
# Last Update:星期五 2017-11-10 10:57:55 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint
from .views import AvatarView, AvatarFileView

site = Blueprint('upload', __name__)
avatar_file_view = AvatarFileView.as_view('avatar_file')
avatar_view = AvatarView.as_view('avatar')

site.add_url_rule('/avatar', view_func=avatar_view)
site.add_url_rule('/avatars/<filename>', view_func=avatar_file_view)


def init_app(app):
    app.register_blueprint(site)
