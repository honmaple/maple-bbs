#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-06-17 13:25:39 (CST)
# Last Update:星期五 2016-6-17 13:36:59 (CST)
#          By:
# Description:
# **************************************************************************
from flask_maple import Auth
from maple import app, mail, db
from maple.user.models import User, UserInfor, UserSetting, Role


class Login(Auth):
    def register_models(self, form):
        user = self.User()
        user.username = form.username.data
        user.password = user.set_password(form.password.data)
        user.email = form.email.data
        userinfor = UserInfor()
        user.infor = userinfor
        usersetting = UserSetting()
        user.setting = usersetting
        role = Role()
        role.rolename = 'unconfirmed'
        user.roles.append(role)
        self.db.session.add(user)
        self.db.session.commit()
        return user

    def confirm_models(self, user):
        user.is_confirmed = True
        self.db.session.commit()


auth = Login(app, db=db, mail=mail, user_model=User, use_principal=True)
