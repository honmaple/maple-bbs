#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: __init__.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-21 21:56:10 (CST)
# Last Update: Monday 2019-05-06 22:59:34 (CST)
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
