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
from wtforms.validators import Length, Required, EqualTo, Email


class RegisterForm(Form):
    name = StringField('用户名:',
                       [Required(message='用户名不能为空'),
                        Length(min=4,
                               max=20,
                               message='用户名长度在4到20个字符之间')])
    email = StringField('邮箱:',
                        [Required(message='邮箱不能为空'),
                         Email(message='错误的邮箱地址')])
    passwd = PasswordField('密码:',
                           [Required(message='密码不能为空'),
                            Length(min=4,
                                   max=20,
                                   message='密码长度在4到20个字符之间')])
    code = StringField('验证码:',
                           [Required(message='验证码不能为空'),
                            Length(min=4, max=4,message='验证码错误')])



class LoginForm(Form):
    name = StringField('用户名:',
                       [Required(message='用户名不能为空'),
                        Length(min=4,
                               max=20,
                               message='用户名长度在4到20个字符之间')])
    passwd = PasswordField('密码:',
                           [Required(message='密码不能为空'),
                            Length(min=4,
                                   max=20,
                                   message='密码长度在4到20个字符之间')])
    code = StringField('验证码:',
                           [Required(message='验证码不能为空'),
                            Length(min=4, max=4,message='验证码错误')])
    remember = BooleanField('remember me', default=False)


class SettingForm(Form):
    introduce = TextAreaField('介绍:',
                              [Length(min=4,
                                      message='个人介绍不能少于4个字符')])
    school = StringField('学校',
                         [Length(min=4,
                                 max=20,
                                 message='学校在4到20个字符之间')])
    word = TextAreaField('签名',
                         [Length(min=4,
                                 message='签名不能少于4个字符')])


class PrivacyForm(Form):
    online_status = SelectField('登录状态',
                                choices=[('所有人', '所有人'), ('已登录用户', '已登录用户'),
                                         ('仅自己', '仅自己')])
    topic_list = SelectField('主题列表',
                             choices=[('所有人', '所有人'), ('已登录用户', '已登录用户'),
                                      ('仅自己', '仅自己')])


class ForgetPasswdForm(Form):
    confirm_email = StringField('注册邮箱:',
                                [Required(message='邮箱不能为空'),
                                 Email(message='错误的邮箱地址')])
    code = StringField('验证码:',
                           [Required(message='验证码不能为空'),
                            Length(min=4, max=4,message='验证码错误')])


class NewPasswdForm(Form):
    passwd = PasswordField('原密码',
                           [Required(message=u'原密码不能为空'),
                            Length(min=4,
                                   max=20,
                                   message='密码长度在4到20个字符之间')])
    npasswd = PasswordField('新密码',
                            [Required(message=u'新密码不能为空'),
                                Length(min=4,
                                       max=20,
                                       message='密码长度在4到20个字符之间'),
                                EqualTo('rpasswd',
                                        message=u'两次密码不一致')])
    rpasswd = PasswordField('重复新密码',
                            [Required(message=u'重复密码不能为空')])
