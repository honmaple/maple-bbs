#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: controls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-06-15 10:03:28 (CST)
# Last Update:星期一 2016-7-25 15:44:44 (CST)
#          By:
# Description:
# **************************************************************************
from flask_login import logout_user, current_user
from maple import db


class SettingModel(object):
    def profile(form):
        infor = current_user.infor
        infor.introduce = form.introduce.data
        infor.school = form.school.data
        infor.word = form.word.data
        db.session.commit()

    def password(form):
        password = form.password.data
        password_n = form.password_n.data
        if current_user.check_password(password):
            current_user.password = current_user.set_password(password_n)
            db.session.commit()
            logout_user()
            return True
        return False

    def privacy(form):
        online_status = form.online_status.data
        topic_list = form.topic_list.data
        rep_list = form.rep_list.data
        ntb_list = form.ntb_list.data
        collect_list = form.collect_list.data
        current_user.setting.online_status = online_status
        current_user.setting.topic_list = topic_list
        current_user.setting.rep_list = rep_list
        current_user.setting.ntb_list = ntb_list
        current_user.setting.collect_list = collect_list
        db.session.commit()

    def babel(form):
        timezone = form.timezone.data
        locale = form.locale.data
        current_user.setting.locale = locale
        current_user.setting.timezone = timezone
        db.session.commit()
