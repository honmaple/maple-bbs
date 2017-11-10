#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-03-31 17:27:30 (CST)
# Last Update:星期五 2017-11-10 10:57:29 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint
from .views import SearchView

site = Blueprint('search', __name__)

site.add_url_rule('/search', view_func=SearchView.as_view('search'))

def init_app(app):
    app.register_blueprint(site)
