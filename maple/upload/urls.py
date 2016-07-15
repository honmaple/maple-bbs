#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-07-15 19:32:23 (CST)
# Last Update:星期五 2016-7-15 19:33:55 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint
from .views import avatar, avatar_file

site = Blueprint('upload', __name__)

site.add_url_rule('/avatar', view_func=avatar, methods=['POST'])
site.add_url_rule('/avatars/<filename>', view_func=avatar_file)
