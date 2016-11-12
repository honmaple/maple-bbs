#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-06-17 13:25:39 (CST)
# Last Update:星期六 2016-11-12 22:16:30 (CST)
#          By:
# Description:
# **************************************************************************
from flask_login import login_required, current_user
from maple.extension import mail, redis_data
from maple.user.models import User, UserInfor, UserSetting, Role
from maple.main.models import set_email_send
from maple.common.response import HTTPResponse
from datetime import datetime, timedelta
from flask_maple.auth import (Auth, RegisterBaseView, ConfirmBaseView,
                              ConfirmTokenBaseView)


def check_time(func):
    def wrapper(*args, **kw):
        time = redis_data.hget('user:%s' % str(current_user.id),
                               'send_email_time')
        if time:
            try:
                time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
                if datetime.utcnow() < time + timedelta(seconds=360):
                    return HTTPResponse(
                        HTTPResponse.USER_EMAIL_WAIT).to_response()
            except TypeError:
                set_email_send(current_user.id)
            except ValueError:
                set_email_send(current_user.id)
        else:
            set_email_send(current_user.id)
        return func(*args, **kw)

    return wrapper


class RegisterView(RegisterBaseView):
    mail = mail
    user_model = User
    use_principal = True

    def register_models(self, form):
        user = self.user_model()
        user.username = form.username.data
        user.password = user.set_password(form.password.data)
        user.email = form.email.data
        userinfor = UserInfor()
        user.infor = userinfor
        usersetting = UserSetting()
        user.setting = usersetting
        role = Role.query.filter_by(name='unconfirmed').first()
        if role is None:
            role = Role()
            role.name = 'unconfirmed'
        user.add()
        return user


class ConfirmTokenView(ConfirmTokenBaseView):
    user_model = User
    mail = mail

    def confirm_models(self, user):
        user.is_confirmed = True
        user.save()


class ConfirmView(ConfirmBaseView):
    decorators = [login_required, check_time]
    mail = mail

    def email_models(self):
        set_email_send(current_user.id)
        # current_user.save()


def register_auth(app):
    auth = Auth(mail=mail, user_model=User, use_principal=True)
    auth.register_view = lambda: RegisterView
    auth.confirm_view = lambda: ConfirmView
    auth.confirm_token_view = lambda: ConfirmTokenView
    auth.init_app(app)
