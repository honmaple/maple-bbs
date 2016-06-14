#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: forms.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 18:08:44 (CST)
# Last Update:星期二 2016-6-14 23:20:13 (CST)
#          By:
# Description:
# **************************************************************************
from flask_wtf import Form
from wtforms import StringField, TextAreaField, SelectField, BooleanField,FieldList
from wtforms.validators import DataRequired, Length, InputRequired
from flask_babel import lazy_gettext as _
from maple.forums.models import Board
from wtforms.ext.sqlalchemy.fields import QuerySelectField


class TopicForm(Form):
    title = StringField(_('Title:'), [DataRequired(), Length(min=4, max=36)])
    content = TextAreaField(_('Content:'), [DataRequired(), Length(min=6)])
    category = SelectField(
        _('Category:'),
        choices=[(b.id, b.board + '   --' + b.parent_board)
                 for b in Board.query.all()],
        coerce=int)
    tags = StringField(_('Tags:'), [DataRequired(), Length(min=2, max=36)])


class ReplyForm(Form):
    content = TextAreaField(_('Content:'), [DataRequired()])
