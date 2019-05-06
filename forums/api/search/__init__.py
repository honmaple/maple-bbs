#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: __init__.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-03-31 17:25:57 (CST)
# Last Update: Monday 2019-05-06 23:00:20 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint
from .views import SearchView

site = Blueprint('search', __name__)

site.add_url_rule('/search', view_func=SearchView.as_view('search'))

def init_app(app):
    app.register_blueprint(site)
