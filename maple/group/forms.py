# !/usr/bin/env python
# -*- coding=UTF-8 -*-
# *************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: forms.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2016-03-16 17:37:48
# *************************************************************************
from flask_wtf import Form
from wtforms import TextAreaField
from maple.forms.forms import DataRequired, Length

class ApplyForm(Form):
    content = TextAreaField('申请理由:', [DataRequired(), Length(min=2,max=255)])
