#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: runserver.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-10-25 22:01:29 (CST)
# Last Update:星期三 2017-1-25 20:12:33 (CST)
#          By:
# Description:
# **************************************************************************
from forums import create_app
from werkzeug.contrib.fixers import ProxyFix

app = create_app()
app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.run()
    # print(app.url_map)
