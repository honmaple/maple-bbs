#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: runserver.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-10-25 22:01:29 (CST)
# Last Update:星期六 2017-4-1 23:10:12 (CST)
#          By:
# Description:
# **************************************************************************
from forums import create_app
from werkzeug.contrib.fixers import ProxyFix

app = create_app('config')
app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.run()
