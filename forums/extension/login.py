#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ********************************************************************************
# Copyright © 2018 jianglin
# File Name: login.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2018-02-11 14:54:38 (CST)
# Last Update: Wednesday 2018-07-25 18:54:54 (CST)
#          By:
# Description:
# ********************************************************************************
from flask_login import LoginManager
from flask_babel import lazy_gettext as _

login_manager = LoginManager()


@login_manager.user_loader
def user_loader(id):
    from forums.api.user.models import User
    user = User.query.get(int(id))
    return user


def init_app(app):
    login_manager.login_view = "auth.login"
    # remember me only work with `basic` rathar than `strong`
    login_manager.session_protection = "basic"
    login_manager.login_message = _("Please login to access this page.")
    # login_manager.anonymous_user = Anonymous
    login_manager.init_app(app)
