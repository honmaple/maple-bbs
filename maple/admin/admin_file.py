#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: admin_file.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-07-02 20:24:36 (CST)
# Last Update:星期六 2016-7-2 20:42:24 (CST)
#          By:
# Description:
# **************************************************************************
from flask_admin.contrib.sqla import ModelView
from flask import Markup, url_for
from flask_admin import form
from maple import db, app
import os.path as op
from maple.user.models import UserInfor

file_path = op.join(app.static_folder, 'avatars')


class ImageView(ModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.avatar:
            return ''

        return Markup('<img src="%s" style="width:120px">' %
                      url_for('upload.avatar_file',
                              filename=model.avatar))

    column_formatters = {'avatar': _list_thumbnail}
    column_list = ['user', 'avatar']
    form_columns = column_list

    form_extra_fields = {
        'avatar': form.ImageUploadField('Avatar',
                                        base_path=file_path,
                                        thumbnail_size=(100, 100, True))
    }


def admin_file(admin):
    admin.add_view(ImageView(
        UserInfor, db.session,
        name='管理头像', category='管理文件'))
