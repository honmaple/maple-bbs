#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: forms.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-21 22:46:35 (CST)
# Last Update:星期一 2016-7-25 17:43:3 (CST)
#          By:
# Description:
# **************************************************************************
from flask_wtf import Form
from flask_babelex import lazy_gettext as _
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import Length, DataRequired, EqualTo
from pytz import all_timezones

choices = [(1, _('Everybody')), (2, _('Logined User')), (3, _('Only Self'))]


class PrivacyForm(Form):
    online_status = SelectField(
        _('Login status:'), coerce=int,
        choices=choices)
    topic_list = SelectField(_('Topic List:'), coerce=int, choices=choices)

    rep_list = SelectField(_('Reply List:'), coerce=int, choices=choices)
    ntb_list = SelectField(_('Notebook List:'), coerce=int, choices=choices)
    collect_list = SelectField(_('Collect List:'), coerce=int, choices=choices)


class ProfileForm(Form):
    introduce = TextAreaField(_('Introduce:'), [Length(max=256)])
    school = StringField(_('School:'), [Length(max=256)])
    word = TextAreaField(_('Signature:'), [Length(max=256)])


class PasswordForm(Form):
    password = PasswordField(
        _('Old Password:'), [DataRequired(), Length(min=4, max=20)])
    password_n = PasswordField(
        _('New Password:'),
        [DataRequired(), Length(min=4, max=20), EqualTo('password_nn')])
    password_nn = PasswordField(_('New Password again:'), [DataRequired()])


class BabelForm(Form):
    timezone = SelectField(
        _('Timezone:'), choices=[(i, i) for i in all_timezones])
    locale = SelectField(
        _('Locale:'),
        choices=[('en', _('English')), ('zh', _('Chinese'))])
