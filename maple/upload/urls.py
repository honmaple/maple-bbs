#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-07-15 19:32:23 (CST)
# Last Update:星期日 2016-11-13 0:15:19 (CST)
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
