#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-07-15 18:17:10 (CST)
# Last Update:星期五 2016-7-15 18:34:33 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint
from .views import tag, rss

site = Blueprint('tag', __name__)

site.add_url_rule('', view_func=tag, defaults={'tag': None})
site.add_url_rule('/<tag>', view_func=tag)
site.add_url_rule('/<tag>/feed', view_func=rss)
