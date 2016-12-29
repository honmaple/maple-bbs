#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-17 13:15:10 (CST)
# Last Update:星期六 2016-12-17 13:15:20 (CST)
#          By:
# Description:
# **************************************************************************
from flask_admin.contrib.sqla import ModelView
from flask_wtf import Form


class BaseForm(Form):
    def __init__(self, formdata=None, obj=None, prefix=u'', **kwargs):
        self._obj = obj
        super(BaseForm, self).__init__(
            formdata=formdata, obj=obj, prefix=prefix, **kwargs)


class BaseView(ModelView):

    page_size = 10
    can_view_details = True
    form_base_class = BaseForm
