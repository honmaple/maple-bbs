#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: response.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-10-25 21:07:00 (CST)
# Last Update: Wednesday 2018-07-25 18:54:54 (CST)
#          By:
# Description:
# **************************************************************************
from flask import jsonify
from flask_babel import gettext as _


class HTTPResponse(object):
    NORMAL_STATUS = '200'
    AUTH_USER_OR_PASSWORD_ERROR = '301'
    AUTH_CAPTCHA_ERROR = '302'
    AUTH_USERNAME_UNIQUE = '303'
    AUTH_EMAIL_UNIQUE = '303'
    AUTH_EMAIL_NOT_REGISTER = '304'
    AUTH_USER_IS_CONFIRMED = '305',
    FORM_VALIDATE_ERROR = '305'
    AUTH_TOKEN_VERIFY_FAIL = '306'

    FORBIDDEN = '403'

    OTHER_ERROR = '500'

    STATUS_DESCRIPTION = {
        NORMAL_STATUS: 'normal',
        AUTH_USER_OR_PASSWORD_ERROR: _('Username or Password Error'),
        AUTH_CAPTCHA_ERROR: _('Captcha Error'),
        AUTH_EMAIL_UNIQUE: _('The email has been registered!'),
        AUTH_USERNAME_UNIQUE: _('The username has been registered!'),
        AUTH_EMAIL_NOT_REGISTER: _('The email is error'),
        AUTH_USER_IS_CONFIRMED:
        _('Your account has been confirmed,don\'t need again!'),
        AUTH_TOKEN_VERIFY_FAIL:
        _('Token is out of time,please get token again!'),
        FORM_VALIDATE_ERROR: _('Form validate error'),
        FORBIDDEN: _('You have no permission!'),
        OTHER_ERROR: _('Other error')
    }

    def __init__(self,
                 status='200',
                 message='',
                 data=None,
                 description='',
                 pageinfo=None):
        self.status = status
        self.message = message or self.STATUS_DESCRIPTION.get(status)
        self.data = data
        self.description = description
        self.pageinfo = pageinfo

    def to_dict(self):
        response = {
            'status': self.status,
            'message': self.message,
            'data': self.data,
            'description': self.description,
        }
        if self.pageinfo is not None:
            response.update(pageinfo=self.pageinfo.as_dict())
        return response

    def to_response(self):
        response = self.to_dict()
        return jsonify(response)
