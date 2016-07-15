#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 18:04:43 (CST)
# Last Update:星期五 2016-7-15 19:31:34 (CST)
#          By:
# Description:
# **************************************************************************
from flask import (render_template, request, g, url_for, redirect, abort,
                   current_app)
from maple.helpers import is_num
from maple.topic.models import Topic, Reply, Collect
from maple.user.models import User


def user():
    topics = Topic.query.join(Topic.author).filter(
        User.username == g.user_url).paginate(1,
                                              current_app.config['PER_PAGE'],
                                              error_out=True)
    data = {'type': 'topic', 'topics': topics}
    return render_template('user/user.html', **data)


def topic():
    orderby = request.args.get('orderby')
    page = is_num(request.args.get('page'))
    all_order = ['vote', 'publish']
    if orderby and orderby not in all_order:
        abort(404)
    if orderby == 'vote':
        topics = Topic.query.join(Topic.author).filter(
            User.username == g.user_url).order_by(Topic.vote.desc()).paginate(
                page,
                current_app.config['PER_PAGE'],
                error_out=True)
    else:
        topics = Topic.query.join(Topic.author).filter(
            User.username == g.user_url).paginate(
                page,
                current_app.config['PER_PAGE'],
                error_out=True)
    data = {'type': 'topic', 'topics': topics}
    return render_template('user/user.html', **data)


def reply():
    page = is_num(request.args.get('page'))
    replies = Reply.query.join(Reply.author).filter(
        User.username == g.user_url).paginate(page,
                                              current_app.config['PER_PAGE'],
                                              error_out=True)
    data = {'type': 'reply', 'replies': replies}
    return render_template('user/user.html', **data)


def collect():
    page = is_num(request.args.get('page'))
    collects = Collect.query.paginate(page,
                                      current_app.config['PER_PAGE'],
                                      error_out=True)
    data = {'type': 'collect', 'collects': collects}
    return render_template('user/user.html', **data)


def following():
    return redirect(url_for('mine.follow'))


def follower():
    page = is_num(request.args.get('page'))
    user = User.query.filter_by(username=g.user_url).first_or_404()
    followers = user.followers.paginate(page,
                                        current_app.config['PER_PAGE'],
                                        error_out=True)
    data = {'type': 'follower', 'followers': followers}
    return render_template('user/user.html', **data)
