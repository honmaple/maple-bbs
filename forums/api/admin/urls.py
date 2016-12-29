#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-10-28 10:15:42 (CST)
# Last Update:星期六 2016-12-17 13:16:28 (CST)
#          By:
# Description:
# **************************************************************************
from maple.extension import admin
from .forums import register_forums
from .permission import register_permission
from .user import register_user
from .topic import register_topic

register_forums(admin)
register_user(admin)
register_topic(admin)
register_permission(admin)
