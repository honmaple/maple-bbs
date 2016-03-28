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
from wtforms import SelectField

#  class SortForm(Form):
#  display = SelectField('筛选',
#  choices=[('全部主题', '全部主题'), ('1天', '1天'),
#  ('1周','1周'),('1个月','1个月')],
#  validators=[DataRequired(message='分类不能为空')])
#  sort = SelectField('排序',choices=[('发表时间', '发表时间'),
#  ('作者','作者')],
#  validators=[DataRequired(message='分类不能为空')])
#  st = SelectField('升降序',choices=[('降序', '降序'), ('升序', '升序')],
#  validators=[DataRequired(message='分类不能为空')])


class SortForm(Form):
    display = SelectField('筛选',
                          coerce=int,
                          choices=[(0, '全部主题'),
                                   (1, '1天'),
                                   (2, '1周'),
                                   (3, '1个月')])
    sort = SelectField('排序',
                       coerce=int,
                       choices=[(0, '发表时间'),
                                (1, '作者')])
    st = SelectField('升降序',
                     coerce=int,
                     choices=[(0, '降序'),
                              (1, '升序')])
