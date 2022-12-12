#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ********************************************************************************
# Copyright © 2018 jianglin
# File Name: maple.py
# Author: jianglin
# Email: mail@honmaple.com
# Created: 2018-02-11 14:56:08 (CST)
# Last Update: Monday 2022-12-12 16:38:21 (CST)
#          By:
# Description:
# ********************************************************************************
from flask_maple.bootstrap import Bootstrap
from flask_maple.captcha import Captcha
from flask_maple.error import Error
from flask_maple.app import App
from flask_maple.json import CustomJSONEncoder
from flask_maple.middleware import Middleware
from flask_maple.log import Logging
from PIL import ImageFont

bootstrap = Bootstrap(css=('styles/monokai.css', 'styles/mine.css'),
                      js=('styles/upload.js', 'styles/forums.js',
                          'styles/following.js', 'styles/topic.js'),
                      use_auth=True)


def init_app(app):
    bootstrap.init_app(app)
    Captcha(app, font=ImageFont.load_default())
    Error(app)
    App(app, json=CustomJSONEncoder)
    Middleware(app)
    Logging(app)
