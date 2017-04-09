#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: __init__.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-01-25 20:10:50 (CST)
# Last Update:星期日 2017-4-9 12:8:22 (CST)
#          By:
# Description:
# **************************************************************************
import os

from flask import Flask

from flask_maple.lazy import LazyExtension
from forums.admin.urls import admin

from .app import register_app
from .filters import register_jinja2
from .logs import register_logging


def create_app(config):
    templates = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, 'templates'))
    static = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, 'static'))

    app = Flask(__name__, template_folder=templates, static_folder=static)
    app.config.from_object(config)
    if app.config['SUBDOMAIN']['forums']:
        app.url_map._rules.clear()
        app.url_map._rules_by_endpoint.clear()
        app.url_map.default_subdomain = 'forums'
        app.add_url_rule(
            app.static_url_path + '/<path:filename>',
            endpoint='static',
            view_func=app.send_static_file,
            subdomain='forums')
    register(app)
    return app


def register(app):
    register_extension(app)
    register_router(app)
    register_logging(app)
    register_jinja2(app)
    register_app(app)


def register_router(app):
    from forums.api.urls import api_routers
    from forums.docs.urls import docs_routers
    api_routers(app)
    docs_routers(app)


def register_extension(app):
    extension = LazyExtension(
        module='forums.extension.',
        extension=['db', 'avatar', 'cache', 'csrf', 'bootstrap', 'captcha',
                   'error', 'redis_data', 'principal', 'babel',
                   'login_manager', 'maple_app', 'mail', 'middleware'])
    extension.init_app(app)
    admin.init_app(app)
