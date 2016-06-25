#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: forms.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-06-25 00:52:30 (CST)
# Last Update:星期六 2016-6-25 0:54:3 (CST)
#          By:
# Description:
# **************************************************************************
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired


class AvatarForm(Form):
    avatar = FileField('上传头像:',
                       validators=[FileRequired(), FileAllowed(
                           ['jpg', 'png'], '上传文件只能为图片且图片格式为jpg,png')])
