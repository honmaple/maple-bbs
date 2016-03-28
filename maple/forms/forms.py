#*************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: forms.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2015-10-29 07:09:54
#*************************************************************************
#!/usr/bin/env python
# -*- coding=UTF-8 -*-
import re
from flask import flash, jsonify
from wtforms.validators import (ValidationError, StopValidation,
                                Regexp, HostnameValidation)
from wtforms.compat import string_types


def flash_errors(form):
    for field, errors in form.errors.items():
        flash(u"%s %s" % (
            getattr(form, field).label.text,
            errors[0]
            ))
        break


def return_errors(form):
    for field, errors in form.errors.items():
        data = (u"%s %s"% (getattr(form, field).label.text, errors[0]))
        break
    return jsonify(judge=False, error=data)


class Length(object):

    def __init__(self, min=-1, max=-1, message=None):
        assert min != -1 or max != -1, 'At least one of `min` or `max` must be specified.'
        assert max == -1 or min <= max, '`min` cannot be more than `max`.'
        self.min = min
        self.max = max
        self.message = message

    def __call__(self, form, field):
        l = field.data and len(field.data) or 0
        if l < self.min or self.max != -1 and l > self.max:
            message = self.message
            if message is None:
                if self.max == -1:
                    message = field.ngettext(
                        '输入长度至少 %(min)d 个字符.',
                        '输入长度至少 %(min)d 个字符.',
                        self.min)
                elif self.min == -1:
                    message = field.ngettext(
                        '输入长度不能超过 %(min)d 个字符.',
                        '输入长度不能超过 %(min)d 个字符.',
                        self.max)
                else:
                    message = field.gettext(
                        '输入长度应在 %(min)d 到 %(max)d 个字符之间.')

            raise ValidationError(
                message %
                dict(
                    min=self.min,
                    max=self.max,
                    length=l))


class DataRequired(object):
    field_flags = ('required', )

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if not field.data or isinstance(
                field.data, string_types) and not field.data.strip():
            if self.message is None:
                message = field.gettext('输入不能为空.')
            else:
                message = self.message

            field.errors[:] = []
            raise StopValidation(message)


class Email(Regexp):

    def __init__(self, message=None):
        self.validate_hostname = HostnameValidation(
            require_tld=True,
        )
        super(Email, self).__init__(r'^.+@([^.@][^@]+)$',
                                    re.IGNORECASE,
                                    message)

    def __call__(self, form, field):
        message = self.message
        if message is None:
            message = field.gettext('错误的邮箱地址.')

        match = super(Email, self).__call__(form, field, message)
        if not self.validate_hostname(match.group(1)):
            raise ValidationError(message)


class EqualTo(object):

    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(
                field.gettext("Invalid field name '%s'.") %
                self.fieldname)
        if field.data != other.data:
            d = {'other_label': hasattr(
                    other,
                    'label') and other.label.text or self.fieldname,
                 'other_name': self.fieldname}
            message = self.message
            if message is None:
                message = field.gettext(
                    '输入必须与 %(other_name)s 相同.')

            raise ValidationError(message % d)
