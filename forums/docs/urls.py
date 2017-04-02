#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-01-25 20:14:36 (CST)
# Last Update:星期日 2017-4-2 12:15:40 (CST)
#          By:
# Description:
# **************************************************************************
from .views import site as docs_site


def docs_routers(app):
    if app.config['SUBDOMAIN']['docs']:
        app.register_blueprint(docs_site, subdomain='docs')
    else:
        app.register_blueprint(docs_site, url_prefix='/docs')
