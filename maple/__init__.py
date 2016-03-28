#!/usr/bin/env python
# -*- coding=UTF-8 -*-
#*************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: app.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2016-03-14 21:04:34
#*************************************************************************
from flask import Flask
from flask_assets import Environment, Bundle
from flask_login import LoginManager, AnonymousUserMixin
from config import load_config
from redis import StrictRedis
from flask_mail import Mail
from flask_principal import Principal
from itsdangerous import URLSafeTimedSerializer
from flask_sqlalchemy import SQLAlchemy


def register_login(app):
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.session_protection = "strong"
    login_manager.login_message = u"这个页面要求登陆，请登陆"
    login_manager.anonymous_user = Anonymous
    login_manager.init_app(app)
    return login_manager


def register_redis(app):
    config = app.config
    redis_data = StrictRedis(db=config['REDIS_DB'],
                             password=config['REDIS_PASSWORD'])
    return redis_data


def register_routes(app):
    from maple.forums.views import site
    app.register_blueprint(site,url_prefix=app.config["FORUMS_URL"])
    from maple.auth.views import site
    app.register_blueprint(site, url_prefix=app.config["AUTH_URL"])
    from maple.question.views import site
    app.register_blueprint(site, url_prefix=app.config["QUESTION_URL"])
    from maple.group.views import site
    app.register_blueprint(site, url_prefix=app.config["USERGROUP_URL"])
    from maple.admin.views import site
    app.register_blueprint(site, url_prefix=app.config["ADMIN_URL"])
    from maple.board.views import site
    app.register_blueprint(site,url_prefix=app.config["BOARD_URL"] + '/<forums_url>')
    from maple.user.views import site
    app.register_blueprint(site, url_prefix=app.config["USER_URL"] + '/<user_url>')


def register_db(app):
    db.init_app(app)


def register_form(app):
    from flask_wtf.csrf import CsrfProtect
    csrf = CsrfProtect()
    csrf.init_app(app)


def register_jinja2(app):
    from maple.main.records import load_online_users
    from maple.main.filters import (safe_markdown,
                                    safe_clean,
                                    join_time,
                                    judge, groups,
                                    load_read_count,
                                    load_user_count,
                                    load_forums_count)
    app.jinja_env.filters['safe_markdown'] = safe_markdown
    app.jinja_env.filters['safe_clean'] = safe_clean
    app.jinja_env.filters['judge'] = judge
    app.jinja_env.filters['groups'] = groups
    app.jinja_env.filters['load_online_users'] = load_online_users
    app.jinja_env.filters['join_time'] = join_time
    app.jinja_env.filters['load_read_count'] = load_read_count
    app.jinja_env.filters['load_user_count'] = load_user_count
    app.jinja_env.filters['load_forums_count'] = load_forums_count


def register_assets(app):
    bundles = {

        'home_js': Bundle(
            'style/js/jquery.min.js',
            'style/js/bootstrap.min.js',
            output='style/assets/home.js',
            filters='jsmin'),

        'home_css': Bundle(
            'style/css/bootstrap.min.css',
            output='style/assets/home.css',
            filters='cssmin')
        }

    assets = Environment(app)
    assets.register(bundles)


class Anonymous(AnonymousUserMixin):
    id = 0
    name = u"Anonymous"
    is_superuser = False


def register(app):
    register_routes(app)
    register_jinja2(app)
    register_assets(app)
    register_db(app)
    register_form(app)


def create_app():
    app = Flask(__name__, static_folder='static')
    config = load_config()
    app.config.from_object(config)
    return app

db = SQLAlchemy()
app = create_app()
mail = Mail(app)
login_manager = register_login(app)
principals = Principal(app)
redis_data = register_redis(app)
login_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
register(app)


from flask import (render_template,g,request,send_from_directory)
from flask_login import current_user

@app.before_request
def before_request():
    g.user = current_user
    from maple.forums.forms import SortForm
    g.sortform = SortForm()
    from maple.main.records import mark_online
    mark_online(request.remote_addr)


@app.errorhandler(404)
def not_found(error):
    return render_template('templet/error_404.html'), 404


@app.route('/robots.txt',methods=['GET'])
@app.route('/favicon.ico',methods=['GET'])
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])
