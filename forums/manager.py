#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: manager.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-10-25 22:08:39 (CST)
# Last Update:星期四 2016-12-29 21:42:7 (CST)
#          By:
# Description:
# **************************************************************************
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from maple import create_app
from maple.extension import db
from api.user.models import User, UserInfo, UserSetting
from getpass import getpass
from werkzeug.security import generate_password_hash
from datetime import datetime
import os

app = create_app()
migrate = Migrate(app, db)
manager = Manager(app)


@manager.command
def runserver():
    return app.run()


@manager.command
def init_db():
    """
    Drops and re-creates the SQL schema
    """
    # db.drop_all()
    db.configure_mappers()
    db.create_all()
    db.session.commit()


@manager.command
def babel_init():
    pybabel = 'pybabel'
    os.system(pybabel +
              ' extract -F babel.cfg -k lazy_gettext -o messages.pot maple')
    os.system(pybabel + ' init -i messages.pot -d translations -l zh')
    os.unlink('messages.pot')


@manager.command
def babel_update():
    pybabel = 'pybabel'
    os.system(
        pybabel +
        ' extract -F babel.cfg -k lazy_gettext -o messages.pot maple templates')
    os.system(pybabel + ' update -i messages.pot -d translations')
    os.unlink('messages.pot')


@manager.command
def babel_compile():
    pybabel = 'pybabel'
    os.system(pybabel + ' compile -d translations')


@manager.option('-u', '--username', dest='username')
@manager.option('-e', '--email', dest='email')
@manager.option('-w', '--password', dest='password')
def create_user(username, email, password):
    if username is None:
        username = input('Username(default admin):') or 'admin'
    if email is None:
        email = input('Email:')
    if password is None:
        password = getpass('Password:')
    user = User()
    user.username = username
    user.password = password
    user.email = email
    user.is_superuser = True
    user.is_confirmed = True
    # user.roles = 'Super'
    # user.confirmed_time = datetime.utcnow()
    db.session.add(user)
    db.session.commit()
    info = UserInfo()
    info.user = user
    setting = UserSetting()
    setting.user = user
    db.session.commit()


@manager.option('-h', '--host', dest='host', default='127.0.0.1')
@manager.option('-p', '--port', dest='port', type=int, default=8000)
@manager.option('-w', '--workers', dest='workers', type=int, default=2)
def gunicorn(host, port, workers):
    """use gunicorn"""
    from gunicorn.app.base import Application

    class FlaskApplication(Application):
        def init(self, parser, opts, args):
            return {'bind': '{0}:{1}'.format(host, port), 'workers': workers}

        def load(self):
            return app

    application = FlaskApplication()
    return application.run()


manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
