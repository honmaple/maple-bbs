#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: __init__.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-03-28 16:23:58 (CST)
# Last Update: Wednesday 2019-05-08 13:24:05 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint
from .views import CollectListView, CollectView, AddToCollectView

site = Blueprint('collect', __name__)


def init_app(app):
    site.add_url_rule('/collect', view_func=CollectListView.as_view('list'))
    site.add_url_rule(
        '/collect/<int:pk>', view_func=CollectView.as_view('collect'))
    site.add_url_rule(
        '/topic/<int:topicId>/collect',
        view_func=AddToCollectView.as_view('add_to_collect'))
    app.register_blueprint(site)
