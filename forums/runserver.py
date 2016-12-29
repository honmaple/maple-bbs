#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: runserver.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-10-25 22:01:29 (CST)
# Last Update:星期四 2016-12-29 20:38:13 (CST)
#          By:
# Description:
# **************************************************************************
from maple import create_app
from werkzeug.contrib.fixers import ProxyFix

app = create_app()
app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.run()
