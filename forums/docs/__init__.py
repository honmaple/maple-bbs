#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: __init__.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-11-09 21:06:11 (CST)
# Last Update:星期二 2017-9-19 12:54:23 (CST)
#          By:
# Description:
# **************************************************************************
from .views import site as docs_site


def init_app(app):
    if app.config['SUBDOMAIN']['docs']:
        app.register_blueprint(docs_site, subdomain='docs')
    else:
        app.register_blueprint(docs_site, url_prefix='/docs')
