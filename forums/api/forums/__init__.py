#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: __init__.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-17 20:44:07 (CST)
# Last Update: Wednesday 2019-05-08 13:18:36 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint

site = Blueprint('forums', __name__)


def init_app(app):
    from .views import (IndexView, AboutView, HelpView, ContactView,
                        BoardListView, BoardView)
    forums_view = BoardListView.as_view('forums')

    site.add_url_rule('/', view_func=IndexView.as_view('index'))
    site.add_url_rule('/about', view_func=AboutView.as_view('about'))
    site.add_url_rule('/help', view_func=HelpView.as_view('help'))
    site.add_url_rule('/contact', view_func=ContactView.as_view('contact'))
    site.add_url_rule('/index', view_func=forums_view)
    site.add_url_rule('/forums', view_func=forums_view)
    site.add_url_rule('/forums/<int:pk>', view_func=BoardView.as_view('board'))

    app.register_blueprint(site)
