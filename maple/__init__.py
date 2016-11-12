#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: __init__.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 12:35:52 (CST)
# Last Update:星期六 2016-11-12 21:43:0 (CST)
#          By:jianglin
# Description:
# **************************************************************************
from flask import Flask
from flask_maple.lazy import LazyExtension
from maple.auth.views import register_auth
from maple.admin.urls import admin
from .filters import register_jinja2
from .logs import register_logging
from .urls import register_routes
from .app import register_app
from .extension import register_rbac
import os


def create_app():
    templates = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, 'templates'))
    static = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, 'static'))

    app = Flask(__name__, template_folder=templates, static_folder=static)
    app.config.from_object('config.config')
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
    register_rbac(app)
    register_jinja2(app)
    register_routes(app)
    register_logging(app)
    register_auth(app)
    register_app(app)


def register_extension(app):
    extension = LazyExtension(
        module='maple.extension.',
        extension=['db', 'avatar', 'cache', 'csrf', 'bootstrap', 'captcha',
                   'error', 'redis_data', 'principal', 'mail', 'babel',
                   'login_manager', 'maple_app', 'middleware'])
    extension.init_app(app)
    admin.init_app(app)
