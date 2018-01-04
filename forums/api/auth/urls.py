#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-10-28 10:26:16 (CST)
# Last Update:星期三 2017-12-13 11:40:54 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint
from .views import (LoginView, LogoutView, RegisterView, ForgetView,
                    ConfirmView, ConfirmTokenView)

__all__ = ['site']

site = Blueprint('auth', __name__)

login_view = LoginView.as_view('login')
logout_view = LogoutView.as_view('logout')
register_view = RegisterView.as_view('register')
forget_view = ForgetView.as_view('forget')
confirm_view = ConfirmView.as_view('confirm')
confirm_token_view = ConfirmTokenView.as_view('confirm_token')

site.add_url_rule('/login', view_func=login_view)
site.add_url_rule('/logout', view_func=logout_view)
site.add_url_rule('/register', view_func=register_view)
site.add_url_rule('/forget', view_func=forget_view)
site.add_url_rule('/confirm', view_func=confirm_view)
site.add_url_rule('/confirm/<token>', view_func=confirm_token_view)


def init_app(app):
    from flask_maple.auth.views import Auth
    Auth(app)
    # app.register_blueprint(site)
