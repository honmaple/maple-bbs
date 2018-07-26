#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: __init__.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-11-09 21:06:11 (CST)
# Last Update: Thursday 2018-07-26 10:03:18 (CST)
#          By:
# Description:
# **************************************************************************
from forums import default
from .views import site as docs_site


def init_app(app):
    app.config.setdefault("SUBDOMAIN", default.SUBDOMAIN)
    if app.config['SUBDOMAIN']['docs']:
        app.register_blueprint(docs_site, subdomain='docs')
    else:
        app.register_blueprint(docs_site, url_prefix='/docs')
