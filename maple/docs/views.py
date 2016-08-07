#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-06-15 00:11:56 (CST)
# Last Update:星期一 2016-8-1 17:16:55 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint, render_template, send_from_directory
from os import path as ph

site = Blueprint('docs',
                 __name__,
                 template_folder='templates',
                 static_folder='static')


@site.route('/')
def docs():
    return render_template('docs/doc_list.html')


@site.route('/flask-maple/<path:path>')
def flask_maple(path):
    return send_from_directory(
        ph.join(site.static_folder, 'flask-maple'), path)


@site.route('/flask-avatar/<path:path>')
def flask_avatar(path):
    return send_from_directory(
        ph.join(site.static_folder, 'flask-avatar'), path)
