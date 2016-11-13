#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-07-15 18:36:33 (CST)
# Last Update:星期日 2016-11-13 9:49:32 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint
from .views import SettingView, PasswordView, PrivacyView, BabelView

site = Blueprint('setting', __name__)
setting_view = SettingView.as_view('setting')
password_view = PasswordView.as_view('password')
privacy_view = PrivacyView.as_view('privacy')
babel_view = BabelView.as_view('babel')

site.add_url_rule('', view_func=setting_view)
site.add_url_rule('/profile', view_func=setting_view)
site.add_url_rule('/password', view_func=password_view)
site.add_url_rule('/privacy', view_func=privacy_view)
site.add_url_rule('/babel', view_func=babel_view)
