#*************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: forms.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2015-10-29 07:09:54
#*************************************************************************
#!/usr/bin/env python
# -*- coding=UTF-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField,\
    TextAreaField, SelectField
from maple.forms.forms import Length, DataRequired, EqualTo, Email


class SettingForm(Form):
    introduce = TextAreaField('个人介绍:',
                              [Length(min=4)])
    school = StringField('所在学校:',
                         [Length(min=4,
                                 max=20)])
    word = TextAreaField('个性签名:',
                         [Length(min=4)])


class PrivacyForm(Form):
    online_status = SelectField('登录状态',
                                coerce=int,
                                choices=[(1, '所有人'), (2, '已登陆用户'),
                                         (3, '仅自己')])
    topic_list = SelectField('主题列表',
                                coerce=int,
                             choices=[(1, '所有人'), (2, '已登陆用户'),
                                      (3, '仅自己')])

    rep_list = SelectField('回复列表',
                                coerce=int,
                           choices=[(1, '所有人'), (2, '已登陆用户'),
                                    (3, '仅自己')])
    ntb_list = SelectField('笔记列表',
                                coerce=int,
                           choices=[(1, '所有人'), (2, '已登陆用户'),
                                    (3, '仅自己')])
    collect_list = SelectField('收藏列表',
                                coerce=int,
                               choices=[(1, '所有人'), (2, '已登陆用户'),
                                        (3, '仅自己')])


class NewPasswdForm(Form):
    passwd = PasswordField('原密码:',
                           [DataRequired(),
                            Length(min=4,
                                   max=20)])
    npasswd = PasswordField('新密码:',
                            [DataRequired(),
                                Length(min=4,
                                       max=20),
                                EqualTo('rpasswd')])
    rpasswd = PasswordField('重复新密码:',
                            [DataRequired()])
