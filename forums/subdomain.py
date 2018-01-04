#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: subdomain.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-11-10 10:52:47 (CST)
# Last Update:星期五 2018-01-05 01:15:15 (CST)
#          By:
# Description:
# **************************************************************************


def init_app(app):
    if app.config['SUBDOMAIN']['forums']:
        app.url_map._rules.clear()
        app.url_map._rules_by_endpoint.clear()
        app.url_map.default_subdomain = 'forums'
        app.add_url_rule(
            app.static_url_path + '/<path:filename>',
            endpoint='static',
            view_func=app.send_static_file,
            subdomain='forums')
