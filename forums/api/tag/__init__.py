#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: __init__.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-15 20:46:19 (CST)
# Last Update: Monday 2019-05-06 23:23:45 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint

site = Blueprint('tag', __name__, url_prefix='/tags')


def init_app(app):
    from .views import TagsListView, TagsView, TagFeedView
    site.add_url_rule('', view_func=TagsListView.as_view('list'))
    site.add_url_rule('/<name>', view_func=TagsView.as_view('tag'))
    site.add_url_rule('/<name>/feed', view_func=TagFeedView.as_view('feed'))

    app.register_blueprint(site)
