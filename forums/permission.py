#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: permission.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-03-28 16:02:43 (CST)
# Last Update:星期二 2017-3-28 16:13:3 (CST)
#          By:
# Description:
# **************************************************************************
from flask_principal import Permission, RoleNeed

super_permission = Permission(RoleNeed('super'))
auth_permission = Permission(RoleNeed('auth'))
