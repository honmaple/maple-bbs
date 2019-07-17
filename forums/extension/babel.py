#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ********************************************************************************
# Copyright © 2018 jianglin
# File Name: babel.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2018-02-11 14:52:25 (CST)
# Last Update: Wednesday 2019-05-08 16:25:29 (CST)
#          By:
# Description:
# ********************************************************************************
from flask import request, g
from flask_babel import Babel
from forums.default import LANGUAGES

babel = Babel()


@babel.localeselector
def locale():
    user = getattr(g, 'user', None)
    if user is not None:
        if request.path.startswith('/admin'):
            return 'zh_Hans_CN'
        if g.user.is_authenticated:
            return user.setting.locale or 'zh'
        return request.accept_languages.best_match(LANGUAGES.keys())


@babel.timezoneselector
def timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        if g.user.is_authenticated:
            return user.setting.timezone or 'UTC'
    return 'UTC'


def init_app(app):
    babel.init_app(app)
