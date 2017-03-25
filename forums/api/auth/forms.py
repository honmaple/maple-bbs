#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: forms.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-10-28 10:35:20 (CST)
# Last Update:星期五 2016-10-28 10:36:9 (CST)
#          By:
# Description:
# **************************************************************************
from flask import session
from flask_wtf import Form
from wtforms import (StringField, PasswordField, BooleanField)
from wtforms.validators import Length, DataRequired, Email
from flask_babelex import lazy_gettext as _


class BaseForm(Form):
    username = StringField(
        _('Username:'), [DataRequired(), Length(
            min=4, max=20)])
    password = PasswordField(
        _('Password:'), [DataRequired(), Length(
            min=4, max=20)])
    captcha = StringField(
        _('Captcha:'), [DataRequired(), Length(
            min=4, max=4)])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        captcha = session['captcha']
        captcha_data = self.captcha.data
        if captcha_data.lower() != captcha.lower():
            self.captcha.errors.append(_('The captcha is error'))
            return False

        return True


class RegisterForm(BaseForm):
    email = StringField(_('Email:'), [DataRequired(), Email()])


class LoginForm(BaseForm):
    remember = BooleanField(_('Remember me'), default=False)
