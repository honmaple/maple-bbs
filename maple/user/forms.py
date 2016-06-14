#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: forms.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 18:08:44 (CST)
# Last Update:星期五 2016-5-20 23:30:7 (CST)
#          By:
# Description:
# **************************************************************************
from flask_wtf import Form
from wtforms import StringField, TextAreaField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_babel import lazy_gettext as _


class ProfileForm(Form):
    introduce = TextAreaField('个人介绍:', [Length(min=4)])
    school = StringField('所在学校:', [Length(min=4, max=20)])
    word = TextAreaField('个性签名:', [Length(min=4)])


class PasswordForm(Form):
    password = PasswordField('原密码:', [DataRequired(), Length(min=4, max=20)])
    password_n = PasswordField('新密码:',
                               [DataRequired(), Length(min=4, max=20),
                                EqualTo('password_nn')])
    password_nn = PasswordField('重复新密码:', [DataRequired()])


class PrivacyForm(Form):
    online_status = SelectField('登录状态',
                                coerce=int,
                                choices=[(1, '所有人'), (2, '已登陆用户'), (3, '仅自己')])
    topic_list = SelectField('主题列表',
                             coerce=int,
                             choices=[(1, '所有人'), (2, '已登陆用户'), (3, '仅自己')])

    rep_list = SelectField('回复列表',
                           coerce=int,
                           choices=[(1, '所有人'), (2, '已登陆用户'), (3, '仅自己')])
    ntb_list = SelectField('笔记列表',
                           coerce=int,
                           choices=[(1, '所有人'), (2, '已登陆用户'), (3, '仅自己')])
    collect_list = SelectField('收藏列表',
                               coerce=int,
                               choices=[(1, '所有人'), (2, '已登陆用户'), (3, '仅自己')])
