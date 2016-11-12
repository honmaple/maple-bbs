#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: extension.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 13:02:50 (CST)
# Last Update:星期六 2016-11-12 22:14:57 (CST)
#          By:
# Description:
# **************************************************************************
from flask import request, g, current_app
from flask_wtf.csrf import CsrfProtect
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_babelex import Babel, Domain
from flask_babelex import lazy_gettext as _
from flask_avatar import Avatar
from flask_maple.app import App
from flask_maple.json import CustomJSONEncoder
from flask_maple.middleware import Middleware
from flask_maple import Bootstrap, Error, Captcha
from flask_maple.redis import Redis
from flask_maple.mail import MapleMail
from flask_maple.rbac import Rbac
from flask_cache import Cache
from flask_principal import Principal
from flask_login import LoginManager
import os


def register_rbac(app):
    from maple.user.models import Role
    from maple.permission.models import Route, Permiss
    from flask_login import current_user
    rbac = Rbac(
        app,
        role_model=Role,
        route_model=Route,
        permission_model=Permiss,
        user_loader=current_user,
        skip_startswith_rules=['/admin', '/static'],
        skip_rules=['topic.topic', 'static_from_root', 'avatar',
                    'upload.avatar_file'])
    return rbac


def register_babel():
    translations = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, 'translations'))
    domain = Domain(translations)
    babel = Babel(default_domain=domain)

    @babel.localeselector
    def get_locale():
        user = getattr(g, 'user', None)
        if user is not None:
            if request.path.startswith('/admin'):
                return 'zh_Hans_CN'
            if g.user.is_authenticated:
                return user.setting.locale or 'zh'
        return request.accept_languages.best_match(current_app.config[
            'LANGUAGES'].keys())

    @babel.timezoneselector
    def get_timezone():
        user = getattr(g, 'user', None)
        if user is not None:
            if g.user.is_authenticated:
                return user.setting.timezone or 'UTC'
        return 'UTC'

    return babel


def register_login():
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.session_protection = "strong"
    login_manager.login_message = _("Please login to access this page.")
    # login_manager.anonymous_user = Anonymous
    from maple.user.models import User

    # @login_manager.token_loader
    # def load_token(token):
    #     max_age = app.config["REMEMBER_COOKIE_DURATION"].total_seconds()
    #     data = login_serializer.loads(token, max_age=max_age)
    #     user = User.load_by_name(data[0])
    #     if user and data[1] == user.password:
    #         return user
    #     return None

    @login_manager.user_loader
    def user_loader(id):
        user = User.query.get(int(id))
        return user

    return login_manager


babel = register_babel()
db = SQLAlchemy()
admin = Admin(name='HonMaple', template_mode='bootstrap3')
avatar = Avatar()
csrf = CsrfProtect()
bootstrap = Bootstrap(
    css=('styles/monokai.css', 'styles/mine.css',
         'tags/css/bootstrap-tokenfield.css', 'select2/css/select2.min.css'),
    js=('styles/upload.js', 'styles/forums.js', 'styles/mine.js',
        'styles/topic.js', 'tags/bootstrap-tokenfield.min.js',
        'select2/js/select2.min.js'),
    use_auth=True)
captcha = Captcha()
error = Error()
redis_data = Redis(decode_responses=True)
cache = Cache()
mail = MapleMail()
principal = Principal()
login_manager = register_login()
maple_app = App(json=CustomJSONEncoder)
middleware = Middleware()
