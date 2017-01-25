#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-17 20:45:08 (CST)
# Last Update:星期日 2016-12-18 18:3:23 (CST)
#          By:
# Description:
# **************************************************************************
from flask import render_template
from flask.views import MethodView
from flask_babelex import gettext as _
from api.topic.models import Topic


class IndexView(MethodView):
    def get(self):
        topics = Topic.query.filter_by(
            is_good=True, is_top=False).paginate(1, 10)
        top_topics = Topic.query.filter_by(is_top=True).limit(5)
        if not topics.items:
            topics = Topic.query.filter_by(is_top=False).paginate(1, 10)
        data = {'title': '', 'topics': topics, 'top_topics': top_topics}
        return render_template('forums/index.html', **data)


class ForumsView(MethodView):
    def get(self):
        return ''


class AboutView(MethodView):
    def get(self):
        data = {'title': _('About - ')}
        return render_template('forums/about.html', **data)


class HelpView(MethodView):
    def get(self):
        data = {'title': _('Help - ')}
        return render_template('forums/help.html', **data)


class ContactView(MethodView):
    def get(self):
        data = {'title': _('Contact - ')}
        return render_template('forums/contact.html', **data)
