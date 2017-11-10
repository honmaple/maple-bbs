#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-17 22:03:40 (CST)
# Last Update:星期五 2017-11-10 10:42:19 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint
from .views import (IndexView, AboutView, HelpView, ContactView, BoardListView,
                    BoardView)

site = Blueprint('forums', __name__)

forums_view = BoardListView.as_view('forums')

site.add_url_rule('/', view_func=IndexView.as_view('index'))
site.add_url_rule('/about', view_func=AboutView.as_view('about'))
site.add_url_rule('/help', view_func=HelpView.as_view('help'))
site.add_url_rule('/contact', view_func=ContactView.as_view('contact'))
site.add_url_rule('/index', view_func=forums_view)
site.add_url_rule('/forums', view_func=forums_view)
site.add_url_rule(
    '/forums/<int:boardId>', view_func=BoardView.as_view('board'))


def init_app(app):
    app.register_blueprint(site)
