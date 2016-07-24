#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-07-15 19:23:48 (CST)
# Last Update:星期日 2016-7-24 14:10:2 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint, abort, g
from maple.user.models import User
from maple.forums.forms import MessageForm
from .views import user, topic, reply, collect, following, follower,collect_detail

site = Blueprint('user', __name__)


@site.before_request
def before():
    g.message_form = MessageForm()


@site.url_value_preprocessor
def pull_user_url(endpoint, values):
    g.user_url = values.pop('user_url')
    user = User.query.filter_by(username=g.user_url).first()
    if user is None:
        abort(404)


@site.url_defaults
def add_user_url(endpoint, values):
    if 'user_url' in values or not g.user_url:
        return
    values['user_url'] = g.user_url


site.add_url_rule('', view_func=user)
site.add_url_rule('/topics', view_func=topic)
site.add_url_rule('/replies', view_func=reply)
site.add_url_rule('/collects', view_func=collect)
site.add_url_rule('/collects/<int:collectId>', view_func=collect_detail)
site.add_url_rule('/following', view_func=following)
site.add_url_rule('/followers', view_func=follower)
