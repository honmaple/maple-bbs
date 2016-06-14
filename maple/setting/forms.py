#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: forms.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-21 22:46:35 (CST)
# Last Update:星期日 2016-6-5 14:7:34 (CST)
#          By:
# Description:
# **************************************************************************
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField,\
    TextAreaField, SelectField
from wtforms.validators import Length, DataRequired, Email, EqualTo


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


class ProfileForm(Form):
    introduce = TextAreaField('个人介绍:',
                              [Length(max=256)])
    school = StringField('所在学校:',
                         [Length(max=256)])
    word = TextAreaField('个性签名:',
                         [Length(max=256)])



class PasswordForm(Form):
    password = PasswordField('原密码:', [DataRequired(), Length(min=4, max=20)])
    password_n = PasswordField('新密码:',
                               [DataRequired(), Length(min=4, max=20),
                                EqualTo('password_nn')])
    password_nn = PasswordField('重复新密码:', [DataRequired()])
