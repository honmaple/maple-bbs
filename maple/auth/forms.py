# *************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: forms.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2015-10-29 07:09:54
# *************************************************************************
# !/usr/bin/env python
# -*- coding=UTF-8 -*-
from flask.ext.wtf import Form
from wtforms import (StringField, PasswordField, BooleanField)
from maple.forms.forms import Length, DataRequired, Email


class BaseForm(Form):
    name = StringField('用户名:',
                       [DataRequired(),
                        Length(min=4,
                               max=20)])
    passwd = PasswordField('密码:',
                           [DataRequired(),
                            Length(min=4,
                                   max=20)])
    code = StringField('验证码:', [DataRequired(), Length(min=4, max=4)])


class RegisterForm(BaseForm):
    email = StringField('邮箱:', [DataRequired(), Email()])


class LoginForm(BaseForm):
    remember = BooleanField('remember me', default=False)


class ForgetPasswdForm(Form):
    confirm_email = StringField('注册邮箱:',
                                [DataRequired(),
                                 Email()])
    code = StringField('验证码:',
                       [DataRequired(), Length(min=4, max=4)])
