#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-11-09 21:06:32 (CST)
# Last Update:星期五 2017-4-21 19:17:46 (CST)
#          By:
# Description:
# **************************************************************************
from flask import (Blueprint, render_template, send_from_directory)
from flask.views import MethodView
import os

site = Blueprint(
    'docs', __name__, template_folder='templates', static_folder='static')


class DocListView(MethodView):
    def get(self):
        docs = [i for i in os.listdir(site.static_folder)]
        return render_template('docs/doc_list.html', docs=docs)


class DocView(MethodView):
    def get(self, path):
        return send_from_directory(site.static_folder, path)


doclist_view = DocListView.as_view('list')
doc_view = DocView.as_view('doc')
site.add_url_rule('/', view_func=doclist_view)
site.add_url_rule('/<path:path>', view_func=doc_view)
