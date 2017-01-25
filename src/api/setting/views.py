#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-20 22:16:04 (CST)
# Last Update:星期三 2017-1-25 20:25:8 (CST)
#          By:
# Description:
# **************************************************************************
from flask import render_template, redirect, url_for, flash
from flask.views import MethodView
from flask_login import current_user, logout_user
from api.setting.forms import (ProfileForm, PasswordForm, PrivacyForm,
                               AvatarForm, BabelForm, error_callback)
from flask_maple.auth.forms import form_validate


class ProfileView(MethodView):
    def get(self):
        form = ProfileForm()
        avatarform = AvatarForm()
        info = current_user.info
        form.introduce.data = info.introduce
        form.school.data = info.school
        form.word.data = info.word
        data = {'form': form, 'avatarform': avatarform}
        return render_template('setting/setting.html', **data)

    @form_validate(ProfileForm, error=error_callback('setting.setting'), f='')
    def post(self):
        form = ProfileForm()
        info = current_user.info
        info.introduce = form.introduce.data
        info.school = form.school.data
        info.word = form.word.data
        info.save()
        return redirect(url_for('setting.setting'))


class PasswordView(MethodView):
    def get(self):
        form = PasswordForm()
        data = {'form': form}
        return render_template('setting/password.html', **data)

    @form_validate(
        PasswordForm, error=error_callback('setting.password'), f='')
    def post(self):
        form = PasswordForm()
        if not current_user.check_password(form.old_password.data):
            flash('原密码错误', 'warning')
        else:
            current_user.set_password(form.new_password.data)
            current_user.save()
            logout_user()
        return redirect(url_for('setting.password'))


class PrivacyView(MethodView):
    def get(self):
        form = PrivacyForm()
        setting = current_user.setting
        form.online_status.data = setting.online_status
        form.topic_list.data = setting.topic_list
        form.rep_list.data = setting.rep_list
        form.ntb_list.data = setting.ntb_list
        form.collect_list.data = setting.collect_list
        return render_template('setting/privacy.html', form=form)

    @form_validate(PrivacyForm, error=error_callback('setting.privacy'), f='')
    def post(self):
        form = PrivacyForm()
        setting = current_user.setting
        setting.online_status = form.online_status.data
        setting.topic_list = form.topic_list.data
        setting.rep_list = form.rep_list.data
        setting.ntb_list = form.ntb_list.data
        setting.collect_list = form.collect_list.data
        setting.save()
        return redirect(url_for('setting.privacy'))


class BabelView(MethodView):
    def get(self):
        form = BabelForm()
        setting = current_user.setting
        form.timezone.data = setting.timezone
        form.locale.data = setting.locale
        return render_template('setting/babel.html', form=form)

    @form_validate(BabelForm, error=error_callback('setting.babel'), f='')
    def post(self):
        form = BabelForm()
        setting = current_user.setting
        setting.timezone = form.timezone.data
        setting.locale = form.locale.data
        setting.save()
        return redirect(url_for('setting.babel'))
