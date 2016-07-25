#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 18:04:43 (CST)
# Last Update:星期一 2016-7-25 18:58:28 (CST)
#          By:jianglin
# Description: user setting include password , infor and privacy
# **************************************************************************
from flask import (render_template, request, url_for, redirect, flash)
from flask_maple.forms import flash_errors
from flask_login import current_user, login_required
from maple.setting.forms import (ProfileForm, PasswordForm, PrivacyForm,
                                 BabelForm)
from maple.upload.forms import AvatarForm
from .controls import SettingModel


@login_required
def setting():
    form = ProfileForm()
    avatarform = AvatarForm()
    if form.validate_on_submit() and request.method == "POST":
        SettingModel.profile(form)
        return redirect(url_for('setting.setting'))
    else:
        if form.errors:
            flash_errors(form)
            return redirect(url_for('setting.setting'))
        infor = current_user.infor
        form.introduce.data = infor.introduce
        form.school.data = infor.school
        form.word.data = infor.word
        data = {'form': form, 'avatarform': avatarform}
        return render_template('setting/setting.html', **data)


@login_required
def password():
    form = PasswordForm()
    if form.validate_on_submit() and request.method == "POST":
        if SettingModel.password(form):
            flash('The password has been updated,Please login', 'info')
            return redirect(url_for('auth.login'))
        else:
            flash('password is error', 'danger')
            return redirect(url_for('setting.password'))
    else:
        if form.errors:
            flash_errors(form)
            return redirect(url_for('setting.password'))
        return render_template('setting/password.html', form=form)


@login_required
def privacy():
    form = PrivacyForm()
    if form.validate_on_submit() and request.method == "POST":
        SettingModel.privacy(form)
        return redirect(url_for('setting.privacy'))
    else:
        if form.errors:
            flash_errors(form)
            return redirect(url_for('setting.privacy'))
        setting = current_user.setting
        form.online_status.data = setting.online_status
        form.topic_list.data = setting.topic_list
        form.rep_list.data = setting.rep_list
        form.ntb_list.data = setting.ntb_list
        form.collect_list.data = setting.collect_list
        return render_template('setting/privacy.html', form=form)


@login_required
def babel():
    form = BabelForm()
    if form.validate_on_submit() and request.method == "POST":
        SettingModel.babel(form)
        return redirect(url_for('setting.babel'))
    else:
        if form.errors:
            flash_errors(form)
            return redirect(url_for('setting.babel'))
        setting = current_user.setting
        form.timezone.data = setting.timezone
        form.locale.data = setting.locale
        return render_template('setting/babel.html', form=form)
