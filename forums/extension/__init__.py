#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ********************************************************************************
# Copyright © 2018 jianglin
# File Name: __init__.py
# Author: jianglin
# Email: mail@honmaple.com
# Created: 2018-02-11 14:52:12 (CST)
# Last Update: Tuesday 2019-05-07 01:05:29 (CST)
#          By:
# Description:
# ********************************************************************************
from flask import request
from flask_wtf.csrf import CSRFProtect
from flask_avatar import Avatar
from flask_maple.models import db
from flask_maple.redis import Redis
from flask_maple.mail import Mail
from flask_principal import Principal
from flask_msearch import Search
from flask_caching import Cache
from . import babel, login, maple

db = db
csrf = CSRFProtect()
redis_data = Redis()
cache = Cache()
mail = Mail()
principal = Principal()
search = Search(db=db)
avatar = Avatar(
    cache=cache.cached(
        timeout=259200, key_prefix=lambda: "avatar:{}".format(request.url)))


def init_app(app):
    db.init_app(app)
    cache.init_app(app)
    avatar.init_app(app)
    csrf.init_app(app)
    principal.init_app(app)
    redis_data.init_app(app)
    mail.init_app(app)
    search.init_app(app)

    babel.init_app(app)
    login.init_app(app)
    maple.init_app(app)
