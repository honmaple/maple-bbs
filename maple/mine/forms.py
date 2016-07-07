#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: forms.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-06-03 21:41:11 (CST)
# Last Update:星期日 2016-7-10 21:11:14 (CST)
#          By:
# Description:
# **************************************************************************
from flask_wtf import Form
from wtforms import (StringField, TextAreaField, SelectField, PasswordField,
                     RadioField)
from wtforms.validators import DataRequired, Length, EqualTo, InputRequired
from flask_babelex import lazy_gettext as _


class CollectForm(Form):
    name = StringField(_('Name:'), [DataRequired()])
    description = TextAreaField(_('Description:'))
    is_privacy = RadioField('Is_privacy:',
                            choices=[(0, 'privacy'), (1, 'public')],
                            coerce=int)
