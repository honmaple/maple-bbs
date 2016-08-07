#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: extensions.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 13:02:50 (CST)
# Last Update:星期日 2016-8-7 14:12:35 (CST)
#          By:
# Description:
# **************************************************************************
from flask import request, g
from flask.json import JSONEncoder
from flask_wtf.csrf import CsrfProtect
from flask_maple import Bootstrap, Error, Captcha
from flask_login import LoginManager
from flask_babelex import Babel, Domain
from flask_babelex import lazy_gettext as _
from flask_mail import Mail
from flask_principal import Principal
from flask_avatar import Avatar
from flask_cache import Cache
from flask_maple.rbac import Rbac
from redis import StrictRedis
import os


def register_avatar(app):
    Avatar(app)


def register_form(app):
    csrf = CsrfProtect()
    csrf.init_app(app)


def register_rbac(app):
    from maple.user.models import Role
    from maple.permission.models import Route, Permiss
    from flask_login import current_user
    rbac = Rbac(app,
                role_model=Role,
                route_model=Route,
                permission_model=Permiss,
                user_loader=current_user,
                skip_startswith_rules=['/admin', '/static'],
                skip_rules=['topic.topic', 'static_from_root', 'avatar',
                            'upload.avatar_file'])
    return rbac


def register_babel(app):
    translations = os.path.abspath(os.path.join(
        os.path.dirname(__file__), os.pardir, 'translations'))
    domain = Domain(translations)
    babel = Babel(default_domain=domain)
    babel.init_app(app)

    # class CustomJSONEncoder(JSONEncoder):
    #     """This class adds support for lazy translation texts to Flask's
    #     JSON encoder. This is necessary when flashing translated texts."""

    #     def default(self, obj):
    #         from speaklater import is_lazy_string
    #         if is_lazy_string(obj):
    #             try:
    #                 return unicode(obj)  # python 2
    #             except NameError:
    #                 return str(obj)  # python 3
    #         return super(CustomJSONEncoder, self).default(obj)

    # app.json_encoder = CustomJSONEncoder

    @babel.localeselector
    def get_locale():
        user = getattr(g, 'user', None)
        if user is not None:
            if request.path.startswith('/admin'):
                return 'zh_Hans_CN'
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
              css=('styles/monokai.css', 'styles/mine.css',
                   'tags/css/bootstrap-tokenfield.css',
                   'select2/css/select2.min.css'),
              js=('styles/upload.js', 'styles/forums.js', 'styles/mine.js',
                  'styles/topic.js', 'tags/bootstrap-tokenfield.min.js',
                  'select2/js/select2.min.js'),
              use_auth=True)
    Captcha(app)
    Error(app)


def register_redis(app):
    redis_data = StrictRedis(db=app.config['CACHE_REDIS_DB'],
                             password=app.config['CACHE_REDIS_PASSWORD'],
                             decode_responses=True)
    return redis_data


def register_cache(app):
    cache = Cache()
    cache.init_app(app)
    return cache


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


def register_principal(app):
    principal = Principal()
    principal.init_app(app)


def register_jinja2(app):
    from .filters import Filters, safe_clean

    app.jinja_env.globals['Title'] = Filters.Title
    app.jinja_env.globals['hot_tags'] = Filters.hot_tags
    app.jinja_env.globals['recent_tags'] = Filters.recent_tags
    app.jinja_env.globals['notice_count'] = Filters.notice_count
    app.jinja_env.globals['show_time'] = Filters.show_time
    app.jinja_env.filters['get_last_reply'] = Filters.get_last_reply
    app.jinja_env.filters['get_user_infor'] = Filters.get_user_infor
    app.jinja_env.filters['get_read_count'] = Filters.get_read_count
    app.jinja_env.filters['timesince'] = Filters.timesince
    app.jinja_env.filters['markdown'] = Filters.safe_markdown
    app.jinja_env.filters['safe_clean'] = safe_clean
    app.jinja_env.filters['is_collected'] = Filters.is_collected
    app.jinja_env.filters['is_online'] = Filters.is_online
