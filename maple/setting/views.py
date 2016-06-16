#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 18:04:43 (CST)
# Last Update:星期四 2016-6-16 18:53:30 (CST)
#          By:jianglin
# Description: user setting include password , infor and privacy
# **************************************************************************
from flask import (Blueprint, render_template, request, url_for, redirect, g,
                   flash)
from flask_maple.forms import flash_errors
from flask_login import current_user, login_required
from maple.setting.forms import ProfileForm, PasswordForm, PrivacyForm
from .controls import SettingModel

site = Blueprint('setting', __name__)


@site.route('', methods=['GET', 'POST'])
@site.route('/profile', methods=['GET', 'POST'])
@login_required
def setting():
    form = ProfileForm()
    infor = current_user.infor
    if form.validate_on_submit() and request.method == "POST":
        SettingModel.profile(form)
        return redirect(url_for('setting.setting'))
    else:
        if form.errors:
            flash_errors(form)
            return redirect(url_for('setting.setting'))
        form.introduce.data = infor.introduce
        form.school.data = infor.school
        form.word.data = infor.word
        return render_template('setting/setting.html', form=form)


@site.route('/password', methods=['GET', 'POST'])
@login_required
def password():
    form = PasswordForm()
    if form.validate_on_submit() and request.method == "POST":
        if SettingModel.password(form):
            flash('The password has been updated,Please login')
            return redirect(url_for('auth.login'))
        else:
            flash('password is error')
            return redirect(url_for('setting.password'))
    else:
        if form.errors:
            flash_errors(form)
            return redirect(url_for('setting.password'))
        return render_template('setting/password.html', form=form)


@site.route('/privacy', methods=['GET', 'POST'])
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
        else:
            form.online_status.data = current_user.setting.online_status
            form.topic_list.data = current_user.setting.topic_list
            form.rep_list.data = current_user.setting.rep_list
            form.ntb_list.data = current_user.setting.ntb_list
            form.collect_list.data = current_user.setting.collect_list
            return render_template('setting/privacy.html', form=form)
