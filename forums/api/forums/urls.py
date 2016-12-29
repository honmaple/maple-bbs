#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-17 22:03:40 (CST)
# Last Update:星期六 2016-12-17 22:4:12 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint
from .views import (IndexView, ForumsView, AboutView, HelpView, ContactView)

site = Blueprint('forums', __name__)

index_view = IndexView.as_view('index')
forums_view = ForumsView.as_view('forums')
about_view = AboutView.as_view('about')
help_view = HelpView.as_view('help')
contact_view = ContactView.as_view('contact')

site.add_url_rule('/', view_func=index_view)
site.add_url_rule('/index', view_func=forums_view)
site.add_url_rule('/about', view_func=about_view)
site.add_url_rule('/help', view_func=help_view)
site.add_url_rule('/contact', view_func=contact_view)
