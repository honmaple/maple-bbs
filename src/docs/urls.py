#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-01-25 20:14:36 (CST)
# Last Update:星期三 2017-1-25 20:27:55 (CST)
#          By:
# Description:
# **************************************************************************
from .views import site as docs_site


def docs_routers(app):
    app.register_blueprint(docs_site)
