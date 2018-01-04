#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: __init__.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-10-28 10:02:51 (CST)
# Last Update:星期五 2017-11-10 11:10:02 (CST)
#          By:
# Description:
# **************************************************************************
from flask_admin import Admin
from forums.admin import forums, user, topic, message
# from forums.admin import permission

admin = Admin(name='HonMaple', template_mode='bootstrap3')


def init_app(app):
    admin.init_app(app)
    forums.init_admin(admin)
    user.init_admin(admin)
    topic.init_admin(admin)
    message.init_admin(admin)
    # permission.init_admin(admin)
