#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-10-28 10:15:42 (CST)
# Last Update:星期六 2017-4-1 18:55:17 (CST)
#          By:
# Description:
# **************************************************************************
from forums.extension import admin
from .forums import register_forums
# from .permission import register_permission
from .user import register_user
from .topic import register_topic
from .message import register_message

register_forums(admin)
register_user(admin)
register_topic(admin)
register_message(admin)
# register_permission(admin)
