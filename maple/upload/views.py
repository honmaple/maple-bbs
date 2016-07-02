#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-06-25 00:50:56 (CST)
# Last Update:星期六 2016-7-2 18:48:40 (CST)
#          By:
# Description:
# **************************************************************************
from flask import (Blueprint, url_for, redirect, flash, send_from_directory)
from flask_maple.forms import flash_errors
from flask_login import login_required
from maple import app
from .forms import AvatarForm
from .controls import UploadModel
import os

site = Blueprint('upload', __name__)


@site.route('/avatar', methods=['POST'])
@login_required
def avatar():
    form = AvatarForm()
    if form.validate_on_submit():
        UploadModel.avatar(form)
        flash('上传成功', 'success')
        return redirect(url_for('setting.setting'))
    else:
        if form.errors:
            flash_errors(form)
        return redirect(url_for('setting.setting'))


@site.route('/avatars/<filename>')
def avatar_file(filename):
    avatar_path = os.path.join(app.static_folder, app.config['AVATAR_FOLDER'])
    if not os.path.exists(os.path.join(avatar_path, filename)):
        avatar_path = os.path.join(app.static_folder, 'images/')
        filename = 'Moo.png'
    return send_from_directory(avatar_path, filename)
