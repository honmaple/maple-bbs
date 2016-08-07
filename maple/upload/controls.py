#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: controls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-06-25 00:54:15 (CST)
# Last Update:星期日 2016-8-7 18:53:44 (CST)
#          By:
# Description:
# **************************************************************************
from flask import request, current_app
from flask_login import current_user
from werkzeug import secure_filename
from maple import db
from time import time
from random import randint
from PIL import Image
import os


class UploadModel(object):
    def avatar(form):
        file = request.files[form.avatar.name]
        filename = secure_filename(file.filename)
        filename = current_user.username + '-' + str(int(time())) + str(
            randint(1000, 9999))
        img = Image.open(file)
        size = 150, 150
        img.thumbnail(size, Image.ANTIALIAS)
        current_app.config.setdefault('AVATAR_FOLDER',
                                      os.path.join(current_app.static_folder,
                                                   'avatars/'))
        avatar_path = current_app.config['AVATAR_FOLDER']
        avatar = os.path.join(avatar_path, filename + '.png')
        if not os.path.exists(avatar_path):
            os.mkdir(avatar_path)
        img.save(avatar)
        img.close()
        infor = current_user.infor
        if infor.avatar:
            ef = os.path.join(avatar_path, infor.avatar)
            if os.path.exists(ef):
                os.remove(ef)
        # file.save(os.path.join(app.static_folder, filename + '.png'))
        infor.avatar = filename + '.png'
        db.session.commit()
