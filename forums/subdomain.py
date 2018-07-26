#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: subdomain.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-11-10 10:52:47 (CST)
# Last Update: Thursday 2018-07-26 10:02:02 (CST)
#          By:
# Description:
# **************************************************************************
from forums import default


def init_app(app):
    app.config.setdefault("SUBDOMAIN", default.SUBDOMAIN)
    if app.config['SUBDOMAIN']['forums']:
        app.url_map._rules.clear()
        app.url_map._rules_by_endpoint.clear()
        app.url_map.default_subdomain = 'forums'
        app.add_url_rule(
            app.static_url_path + '/<path:filename>',
            endpoint='static',
            view_func=app.send_static_file,
            subdomain='forums')
