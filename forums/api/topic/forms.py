#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: forms.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-18 18:49:00 (CST)
# Last Update:星期六 2017-3-25 21:47:25 (CST)
#          By:
# Description:
# **************************************************************************
from flask import request, render_template, redirect, url_for
from flask_wtf import Form
from wtforms import (StringField, TextAreaField, SelectField, RadioField)
from wtforms.validators import DataRequired, Length
from flask_babelex import lazy_gettext as _
from forums.api.forums.models import Board
from .models import Topic


def error_callback():
    return redirect(url_for('topic.ask'))


def collect_error_callback():
    return redirect(url_for('topic.collectlist'))


def form_board():
    form = TopicForm()
    results = []
    for b in Board.query.filter_by(parent_id=None):
        if b.parent is None:
            results.append((b.id, b.name))
        else:
            results.append((b.id, b.name + '   --' + b.parent.name))
    form.category.choices = results
    return form


class TopicForm(Form):
    title = StringField(_('Title:'), [DataRequired(), Length(min=4, max=36)])
    content = TextAreaField(_('Content:'), [DataRequired(), Length(min=6)])
    category = SelectField(_('Category:'), coerce=int)
    tags = StringField(_('Tags:'), [DataRequired(), Length(min=2, max=36)])
    content_type = SelectField(
        _('ContentType'), choices=Topic.CONTENT_TYPE, coerce=str)


class ReplyForm(Form):
    content = TextAreaField(_('Content:'), [DataRequired()])


class CollectForm(Form):
    name = StringField(_('Name:'), [DataRequired()])
    description = TextAreaField(_('Description:'))
    private = RadioField(
        'Private:', choices=[(0, 'privacy'), (1, 'public')], coerce=int)
