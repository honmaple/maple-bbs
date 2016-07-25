#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 18:04:43 (CST)
# Last Update:星期一 2016-7-25 20:57:42 (CST)
#          By:
# Description:
# **************************************************************************
from flask import (render_template, request, g, url_for, redirect, abort,
                   current_app)
from flask_login import current_user
from maple.helpers import is_num
from maple.topic.models import Topic, Reply, Collect, Like
from maple.user.models import User
from sqlalchemy.sql import func


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
                page, current_app.config['PER_PAGE'],
                error_out=True)
    else:
        topics = Topic.query.join(Topic.author).filter(
            User.username == g.user_url).paginate(
                page, current_app.config['PER_PAGE'],
                error_out=True)
    data = {'type': 'topic', 'topics': topics}
    return render_template('user/user.html', **data)


def reply():
    order = request.args.get('orderby')
    page = is_num(request.args.get('page'))
    all_order = ['like', 'publish']
    if order and order not in all_order:
        abort(404)
    if order == 'like':
        user = User.query.filter_by(username=g.user_url).first_or_404()
        replies = Reply.query.outerjoin(Like).filter(
            Reply.author_id == user.id).group_by(Reply.id).order_by(func.count(
                Like.id).desc()).paginate(page, current_app.config['PER_PAGE'],
                                          True)
    else:
        replies = Reply.query.join(Reply.author).filter(
            User.username == g.user_url).paginate(
                page, current_app.config['PER_PAGE'],
                error_out=True)
    data = {'type': 'reply', 'replies': replies}
    return render_template('user/user.html', **data)


def collect():
    page = is_num(request.args.get('page'))
    per_page = current_app.config['PER_PAGE']
    if current_user.is_authenticated and current_user.username == g.user_url:
        collects = current_user.collects.paginate(
            page, per_page, error_out=True)
    else:
        collects = Collect.query.join(Collect.author).filter(
            Collect.is_privacy == False, User.username == g.user_url).paginate(
                page, per_page, error_out=True)
    data = {'type': 'collect', 'collects': collects}
    return render_template('user/user.html', **data)


def collect_detail(collectId):
    page = is_num(request.args.get('page'))
    per_page = current_app.config['PER_PAGE']
    if current_user.is_authenticated:
        collect = Collect.query.join(Collect.author).filter(
            Collect.id == collectId,
            User.username == g.user_url).first_or_404()
    else:
        collect = Collect.query.join(Collect.author).filter(
            Collect.id == collectId, Collect.is_privacy == False,
            User.username == g.user_url).first_or_404()
    topics = collect.topics.paginate(page, per_page, True)
    data = {'type': 'collect_detail', 'topics': topics, 'collect': collect}
    return render_template('user/user.html', **data)


def following():
    return redirect(url_for('mine.follow'))


def follower():
    page = is_num(request.args.get('page'))
    order = request.args.get('orderby')
    order_list = ['publish', 'score']
    if order and order not in order_list:
        abort(404)
    user = User.query.filter_by(username=g.user_url).first_or_404()
    followers = user.followers.paginate(page,
                                        current_app.config['PER_PAGE'],
                                        error_out=True)
    data = {'type': 'follower', 'followers': followers}
    return render_template('user/user.html', **data)
