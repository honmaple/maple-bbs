#*************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: askform.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2015-11-27 17:54:07
#*************************************************************************
#!/usr/bin/env python
# -*- coding=UTF-8 -*-
from flask_wtf import Form
from wtforms import StringField, TextAreaField, SelectField
from maple.forms.forms import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired


class QuestionForm(Form):
    title = StringField('标题:',
                        [DataRequired(),
                         Length(min=4, max=36)])
    content = TextAreaField('问题描述:',
                            [DataRequired(),
                             Length(min=6)])
    choice = SelectField('文本标记语法',
                         choices=[('Default', 'Default'),
                                  ('Markdown', 'Markdown')])
    tags = StringField('节点:',
                       [DataRequired(),
                        Length(min=2, max=36)])


class PhotoForm(Form):
    photo = FileField('上传图片',
                      validators=[FileRequired(), FileAllowed(
                          ['jpg', 'png'], '只能为图片')])

class ReplyForm(Form):
    content = TextAreaField('回复:',
                            [DataRequired(),
                             Length(min=4)])
