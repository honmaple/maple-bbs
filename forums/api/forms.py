#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: forms.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-03-28 12:53:02 (CST)
# Last Update:星期三 2017-3-29 22:51:17 (CST)
#          By:
# Description:
# **************************************************************************
from flask import redirect, session, url_for
from flask_babelex import lazy_gettext as _
from flask_wtf import FlaskForm as Form
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import (BooleanField, PasswordField, RadioField, SelectField,
                     StringField, TextAreaField)
from wtforms.validators import DataRequired, Email, EqualTo, Length

from forums.api.forums.models import Board
from forums.api.topic.models import Topic
from forums.api.user.models import UserSetting


def error_callback():
    return redirect(url_for('topic.ask'))


def collect_error_callback():
    return redirect(url_for('collect.list'))


def form_board():
    form = TopicForm()
    results = []
    for b in Board.query.all():
        if b.parent is None:
            results.append((b.id, b.name))
        else:
            results.append((b.id, b.name + '   --' + b.parent.name))
    form.category.choices = results
    return form


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


WITHIN = [(0, _('All Topics')), (1, _('One Day')), (2, _('One Week')),
          (3, _('One Month'))]

ORDERBY = [(0, _('Publish')), (1, _('Author'))]

DESC = [(0, _('Desc')), (1, _('Asc'))]


class SortForm(Form):
    within = SelectField(_('Choice'), coerce=int, choices=WITHIN)
    orderby = SelectField('orderby', coerce=int, choices=ORDERBY)
    desc = SelectField('Up and Down', coerce=int, choices=DESC)


class SearchForm(Form):
    search = StringField(_('search'), validators=[DataRequired()])


class MessageForm(Form):
    message = TextAreaField(_('message'), validators=[DataRequired()])


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
    is_hidden = RadioField(
        'Is_hidden:', choices=[(0, 'is_hidden'), (1, 'is_public')], coerce=int)


choices = UserSetting.STATUS
timezone = UserSetting.TIMEZONE
locale = UserSetting.LOCALE


class AvatarForm(Form):
    avatar = FileField(
        _('Upload Avatar:'),
        validators=[FileRequired(), FileAllowed(['jpg', 'png'],
                                                '上传文件只能为图片且图片格式为jpg,png')])


class PrivacyForm(Form):
    online_status = SelectField(
        _('Online status:'), coerce=str, choices=choices)
    topic_list = SelectField(_('Topic List:'), coerce=str, choices=choices)

    rep_list = SelectField(_('Reply List:'), coerce=str, choices=choices)
    ntb_list = SelectField(_('Notebook List:'), coerce=str, choices=choices)
    collect_list = SelectField(_('Collect List:'), coerce=str, choices=choices)


class ProfileForm(Form):
    introduce = TextAreaField(_('Introduce:'), [Length(max=256)])
    school = StringField(_('School:'), [Length(max=256)])
    word = TextAreaField(_('Signature:'), [Length(max=256)])


class PasswordForm(Form):
    old_password = PasswordField(
        _('Old Password:'), [DataRequired(), Length(
            min=4, max=20)])
    new_password = PasswordField(
        _('New Password:'), [DataRequired(), Length(
            min=4, max=20)])
    rnew_password = PasswordField(
        _('New Password again:'), [DataRequired(), EqualTo('new_password')])


class BabelForm(Form):
    timezone = SelectField(_('Timezone:'), coerce=str, choices=timezone)
    locale = SelectField(_('Locale:'), coerce=str, choices=locale)
