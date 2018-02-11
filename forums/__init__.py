#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: __init__.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-01-25 20:10:50 (CST)
# Last Update: 星期日 2018-02-11 15:05:26 (CST)
#          By:
# Description:
# **************************************************************************
import os

from flask import Flask

from forums import app as ap, extension
from forums import jinja, subdomain
from forums import api, docs, admin
from flask_maple import auth


def create_app(config):
    templates = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, 'templates'))
    static = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, 'static'))

    app = Flask(__name__, template_folder=templates, static_folder=static)
    app.config.from_object(config)

    subdomain.init_app(app)
    ap.init_app(app)
    jinja.init_app(app)
    extension.init_app(app)
    admin.init_app(app)
    # router
    auth.init_app(app)
    api.init_app(app)
    docs.init_app(app)
    return app
