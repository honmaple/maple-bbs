#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 18:04:43 (CST)
# Last Update:星期二 2016-6-14 23:20:14 (CST)
#          By:
# Description:
# **************************************************************************
from flask import (Blueprint, render_template, request, g, url_for, redirect,
                   abort)
from maple import app
from maple.helpers import is_num
from maple.topic.models import Topic, Reply, Collect
from maple.user.models import User

site = Blueprint('user', __name__)


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


@site.route('')
def user():
    topics = Topic.query.join(Topic.author).filter(
        User.username == g.user_url).paginate(1,
                                              app.config['PER_PAGE'],
                                              error_out=True)
    data = {'type': 'topic', 'topics': topics}
    return render_template('user/user.html', **data)


@site.route('/topics')
def topic():
    page = is_num(request.args.get('page'))
    topics = Topic.query.join(Topic.author).filter(
        User.username == g.user_url).paginate(page,
                                              app.config['PER_PAGE'],
                                              error_out=True)
    data = {'type': 'topic', 'topics': topics}
    return render_template('user/user.html', **data)


@site.route('/replies')
def reply():
    page = is_num(request.args.get('page'))
    replies = Reply.query.join(Reply.author).filter(
        User.username == g.user_url).paginate(page,
                                              app.config['PER_PAGE'],
                                              error_out=True)
    data = {'type': 'reply', 'replies': replies}
    return render_template('user/user.html', **data)


@site.route('/collects')
def collect():
    page = is_num(request.args.get('page'))
    collects = Collect.query.paginate(page,
                                      app.config['PER_PAGE'],
                                      error_out=True)
    data = {'type': 'collect', 'collects': collects}
    return render_template('user/user.html', **data)


@site.route('/following')
def following():
    return redirect(url_for('mine.follow'))


@site.route('/followers')
def follower():
    page = is_num(request.args.get('page'))
    user = User.query.filter_by(username=g.user_url).first_or_404()
    followers = user.followers.paginate(page,
                                        app.config['PER_PAGE'],
                                        error_out=True)
    data = {'type': 'follower', 'followers': followers}
    return render_template('user/user.html', **data)
