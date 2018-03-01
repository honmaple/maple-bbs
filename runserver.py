#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: runserver.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-10-25 22:01:29 (CST)
# Last Update: 星期五 2018-02-23 10:43:07 (CST)
#          By:
# Description:
# **************************************************************************
from flask import current_app
from flask.cli import FlaskGroup, run_command
from werkzeug.contrib.fixers import ProxyFix
from code import interact
from getpass import getpass

from forums import create_app
from forums.extension import db, cache, search
from forums.api.user.models import User

import click
import os
import sys

app = create_app('config')
app.wsgi_app = ProxyFix(app.wsgi_app)

cli = FlaskGroup(add_default_commands=False, create_app=lambda r: app)
cli.add_command(run_command)

try:
    from flask_migrate import Migrate
    migrate = Migrate(app, db)
except ImportError:
    pass


@cli.command('shell', short_help='Starts an interactive shell.')
def shell_command():
    ctx = current_app.make_shell_context()
    interact(local=ctx)


@cli.command()
def runserver():
    app.run()


@cli.command()
def create_index():
    return search.create_index()


@cli.command()
def update_index():
    return search.create_index(update=True)


@cli.command()
def delete_index():
    return search.create_index(delete=True)


@cli.command()
def clear_cache():
    cache.clear()


@cli.command()
def init_perm():
    from forums.api.user.models import Group
    anonymous = Group.query.filter_by(name='anonymous').first()
    if not anonymous:
        anonymous = Group(name='anonymous')
        anonymous.save()
    logined = Group.query.filter_by(name='logined').first()
    if not logined:
        logined = Group(name='logined')
        logined.save()
    for rule in app.url_map.iter_rules():
        # print(rule.rule, rule.subdomain, rule.methods, rule.endpoint)
        print(rule.endpoint)
        methods = []
        for method in rule.methods:
            methods.append(method)
            method = 'get' if method in ['HEAD', 'OPTIONS'] else method.lower()
            if not rule.endpoint.startswith('admin'):
                anonymous.add_perm(
                    method,
                    rule.endpoint,
                    description='anonymous组允许{}'.format(methods))
                logined.add_perm(
                    method,
                    rule.endpoint,
                    description='logined组允许{}'.format(methods))


@cli.command()
def initdb():
    """
    Drops and re-creates the SQL schema
    """
    db.drop_all()
    db.configure_mappers()
    db.create_all()
    db.session.commit()


@cli.command()
@click.option('-l', '--lang', default='zh')
def babel_init(lang):
    babel_conf = "translations/babel.cfg"
    src_path = ["forums", "templates"]
    os.system('pybabel extract -F {0} -k lazy_gettext -o messages.pot {1}'.
              format(babel_conf, ' '.join(src_path)))
    os.system('pybabel init -i messages.pot -d translations -l {0}'.format(
        lang))
    os.unlink('messages.pot')


@cli.command()
def babel_update():
    babel_conf = "translations/babel.cfg"
    src_path = ["forums", "templates"]
    os.system('pybabel extract -F {0} -k lazy_gettext -o messages.pot {1}'.
              format(babel_conf, ' '.join(src_path)))
    os.system('pybabel update -i messages.pot -d translations')
    os.unlink('messages.pot')


@cli.command()
def babel_compile():
    os.system('pybabel compile -d translations')


@cli.command()
@click.option('-u', '--username')
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    user.delete()


@cli.command()
@click.option('-u', '--username')
def password_user(username):
    password = getpass('Password:')
    user = User.query.filter_by(username=username).first()
    user.set_password(password)
    user.save()


@cli.command()
@click.option('-u', '--username')
@click.option('-e', '--email')
@click.option('-w', '--password')
def create_user(username, email, password):
    if username is None:
        username = input('Username(default admin):') or 'admin'
    if email is None:
        email = input('Email:')
    if password is None:
        password = getpass('Password:')
    user = User(
        username=username, email=email, is_superuser=True, is_confirmed=True)
    user.set_password(password)
    user.save()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        app.run()
    else:
        cli.main()
