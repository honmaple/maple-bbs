#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 18:04:43 (CST)
# Last Update:星期日 2016-11-13 9:51:13 (CST)
#          By:jianglin
# Description: user setting include password , infor and privacy
# **************************************************************************
from flask import (render_template, url_for, redirect, flash)
from flask.views import MethodView
from flask_maple.forms import flash_errors
from flask_login import current_user, login_required
from maple.setting.forms import (ProfileForm, PasswordForm, PrivacyForm,
                                 BabelForm)
from maple.upload.forms import AvatarForm
from .controls import SettingModel


class SettingView(MethodView):
    decorators = [login_required]

    def get(self):
        form = ProfileForm()
        avatarform = AvatarForm()
        infor = current_user.infor
        form.introduce.data = infor.introduce
        form.school.data = infor.school
        form.word.data = infor.word
        data = {'form': form, 'avatarform': avatarform}
        return render_template('setting/setting.html', **data)

    def post(self):
        form = ProfileForm()
        if form.validate_on_submit():
            SettingModel.profile(form)
        else:
            if form.errors:
                flash_errors(form)
        return redirect(url_for('setting.setting'))


class PasswordView(MethodView):
    decorators = [login_required]

    def get(self):
        form = PasswordForm()
        return render_template('setting/password.html', form=form)

    def post(self):
        form = PasswordForm()
        if form.validate_on_submit():
            if SettingModel.password(form):
                flash('The password has been updated,Please login', 'info')
                return redirect(url_for('auth.login'))
            else:
                flash('password is error', 'danger')
        else:
            if form.errors:
                flash_errors(form)
        return redirect(url_for('setting.password'))


class PrivacyView(MethodView):
    decorators = [login_required]

    def get(self):
        form = PrivacyForm()
        setting = current_user.setting
        form.online_status.data = setting.online_status
        form.topic_list.data = setting.topic_list
        form.rep_list.data = setting.rep_list
        form.ntb_list.data = setting.ntb_list
        form.collect_list.data = setting.collect_list
        return render_template('setting/privacy.html', form=form)

    def post(self):
        form = PrivacyForm()
        if form.validate_on_submit():
            SettingModel.privacy(form)
        else:
            if form.errors:
                flash_errors(form)
        return redirect(url_for('setting.privacy'))


class BabelView(MethodView):
    decorators = [login_required]

    def get(self):
        form = BabelForm()
        setting = current_user.setting
        form.timezone.data = setting.timezone
        form.locale.data = setting.locale
        return render_template('setting/babel.html', form=form)

    def post(self):
        form = BabelForm()
        if form.validate_on_submit():
            SettingModel.babel(form)
        else:
            if form.errors:
                flash_errors(form)
        return redirect(url_for('setting.babel'))
