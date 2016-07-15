#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-07-10 22:49:18 (CST)
# Last Update:星期五 2016-7-15 20:49:14 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint, render_template

site = Blueprint('install',
                 __name__,
                 static_folder='static',
                 template_folder='templates')


@site.route('')
def install():
    return render_template('install/start.html')
