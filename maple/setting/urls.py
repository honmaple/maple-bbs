#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-07-15 18:36:33 (CST)
# Last Update:星期一 2016-7-25 15:34:19 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint
from .views import setting, password, privacy, babel

site = Blueprint('setting', __name__)

site.add_url_rule('', view_func=setting, methods=['GET', 'POST'])
site.add_url_rule('/profile', view_func=setting, methods=['GET', 'POST'])
site.add_url_rule('/password', view_func=password, methods=['GET', 'POST'])
site.add_url_rule('/privacy', view_func=privacy, methods=['GET', 'POST'])
site.add_url_rule('/babel', view_func=babel, methods=['GET', 'POST'])
