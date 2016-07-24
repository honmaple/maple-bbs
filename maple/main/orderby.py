#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: orderby.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-06-05 10:15:58 (CST)
# Last Update:星期三 2016-7-20 17:12:4 (CST)
#          By:
# Description:
# **************************************************************************
from flask import request, current_app
from maple.forums.models import Board
from maple.topic.models import Topic
from maple.tag.models import Tags
from datetime import datetime, timedelta


def form_judge(form):
    '''
    0: all topic
    1: one day
    2: one week
    3: one month

    0: time
    1: author

    0: desc
    1: asc
    '''
    t1 = form.display.data
    t2 = form.sort.data
    t3 = form.st.data
    data = form_sort(t1, t2, t3)
    return data


def form_sort(t1, t2, t3):
    orderby = request.get_json()
    type = orderby['type']
    uid = orderby['uid']
    page = int(orderby['page'])

    if t1 == 0:
        time = datetime.now() - timedelta(days=365)
    elif t1 == 1:
        time = datetime.now() - timedelta(days=1)
    elif t1 == 2:
        time = datetime.now() - timedelta(days=7)
    else:
        time = datetime.now() - timedelta(days=30)

    # 发表时间或作者
    if t2 == 0:
        order = Topic.publish
    else:
        order = Topic.author_id

    # 升降序
    if t3 == 0:
        order = order.desc()
    else:
        order = order.asc()

    app = current_app._get_current_object()
    per_page = app.config['PER_PAGE']
    topic_base = Topic.query.join(Topic.board).filter(Topic.publish > time,
                                                      Topic.is_top == False)
    if type == 'parent_b':
        topics = topic_base.filter(Board.parent_board == uid).order_by(
            order).paginate(page, per_page, True)
    elif type == 'child_b':
        topics = topic_base.filter(Board.id == uid).order_by(order).paginate(
            page, per_page, True)
    elif type == 'tags':
        topics = Topic.query.join(Topic.tags).filter(
            Topic.publish > time, Topic.is_top == False,
            Tags.tagname == uid).order_by(order).paginate(page, per_page, True)
    elif type == 'all':
        topics = Topic.query.filter(
            Topic.publish > time,
            Topic.is_top == False).order_by(order).paginate(page, per_page,
                                                            True)
    else:
        topics = None
    return topics
