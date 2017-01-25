#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-11-07 21:00:37 (CST)
# Last Update:星期三 2017-1-25 20:16:33 (CST)
#          By:
# Description:
# **************************************************************************
from api.urls import api_routers
from docs.urls import docs_routers


def register_routes(app):
    api_routers(app)
    docs_routers(app)
