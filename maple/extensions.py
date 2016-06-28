#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: extensions.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 13:02:50 (CST)
# Last Update:星期一 2016-6-27 17:17:11 (CST)
#          By:
# Description:
# **************************************************************************
from flask import request, g
from flask.json import JSONEncoder
from flask_wtf.csrf import CsrfProtect
from flask_maple import Bootstrap, Error, Captcha
from flask_login import LoginManager
from flask_babel import Babel
from flask_babel import lazy_gettext as _
from flask_mail import Mail
from flask_principal import Principal
from redis import StrictRedis


def register_form(app):
    csrf = CsrfProtect()
    csrf.init_app(app)


def register_babel(app):
    babel = Babel()
    babel.init_app(app)

    class CustomJSONEncoder(JSONEncoder):
        """This class adds support for lazy translation texts to Flask's
        JSON encoder. This is necessary when flashing translated texts."""

        def default(self, obj):
            from speaklater import is_lazy_string
            if is_lazy_string(obj):
                try:
                    return unicode(obj)  # python 2
                except NameError:
                    return str(obj)  # python 3
            return super(CustomJSONEncoder, self).default(obj)

    app.json_encoder = CustomJSONEncoder

    @babel.localeselector
    def get_locale():
        user = getattr(g, 'user', None)
        if user is not None:
            if g.user.is_authenticated:
                return user.setting.locale or 'zh'
        return request.accept_languages.best_match(app.config[
            'LANGUAGES'].keys())

    @babel.timezoneselector
    def get_timezone():
        user = getattr(g, 'user', None)
        if user is not None:
            if g.user.is_authenticated:
                return user.setting.timezone or 'UTC'
        return 'UTC'


def register_maple(app):
    Bootstrap(app,
              css=('styles/monokai.css', 'styles/mine.css'),
              js=('styles/upload.js', 'styles/order.js', 'styles/mine.js',
                  'styles/topic.js'),
              use_auth=True)
    Captcha(app)
    Error(app)


def register_principal(app):
    principal = Principal()
    principal.init_app(app)


def register_mail(app):
    mail = Mail()
    mail.init_app(app)
    return mail


def register_login(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
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


def register_redis(app):
    redis_data = StrictRedis(db=app.config['CACHE_REDIS_DB'],
                             password=app.config['CACHE_REDIS_PASSWORD'])
    return redis_data


def register_jinja2(app):
    from maple.main.records import load_online_users
    from .filters import Filters, safe_clean

    app.jinja_env.globals['Title'] = Filters.Title
    app.jinja_env.filters['get_last_reply'] = Filters.get_last_reply
    app.jinja_env.filters['get_user_infor'] = Filters.get_user_infor
    app.jinja_env.filters['get_read_count'] = Filters.get_read_count
    app.jinja_env.filters['timesince'] = Filters.timesince
    app.jinja_env.filters['get_online_users'] = load_online_users
    app.jinja_env.filters['markdown'] = Filters.safe_markdown
    app.jinja_env.filters['safe_clean'] = safe_clean
    app.jinja_env.filters['is_collected'] = Filters.is_collected
