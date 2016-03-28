#*************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: forms.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2015-10-29 07:09:54
#*************************************************************************
#!/usr/bin/env python
# -*- coding=UTF-8 -*-
from flask_wtf import Form
from wtforms import BooleanField, SelectField, StringField, TextAreaField
from wtforms.validators import Required, Length


class AdminForm(Form):
    delete = BooleanField('多选:', default=False)


class AdminUserForm(Form):
    name = StringField('用户名', [Length(min=4, max=25)])
    score = StringField('用户积分')
    is_superuser = SelectField('是否授予超级管理员权限',
                               choices=[('True', 'True'), ('False', 'False')],
                               validators=[Required()])
    roles = SelectField('用户组',
                        choices=[('superadmin', 'superadmin'),
                                 ('admin', 'admin'),
                                 ('writer', 'writer'),
                                 ('editor', 'editor'),
                                 ('visitor', 'visitor')],
                        validators=[Required()])
    is_confirmed = SelectField('修改用户验证状态',
                               choices=[('True', 'True'), ('False', 'False')],

                               validators=[Required()])


class CreateUserForm(Form):
    name = StringField('用户名', [Length(min=4, max=25)])
    email = StringField('邮箱', [Length(min=4, max=25)])
    is_superuser = SelectField('是否授予超级管理员权限',
                               default='False',
                               choices=[('True', 'True'), ('False', 'False')],
                               validators=[Required()])


class CreateGroupForm(Form):
    name = StringField('用户组名',
                       [Required(message='用户组名不能为空'),
                        Length(min=4, max=16)])
    introduce = TextAreaField('用户组描述', [Required(), Length(min=6, max=100)])


class AdminGroupForm(Form):
    member = StringField('用户组成员',
                         [Required(),
                          Length(min=4, max=16)])
