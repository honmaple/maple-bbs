#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: orderby.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-06-05 10:15:58 (CST)
# Last Update:星期六 2016-6-25 18:30:13 (CST)
#          By:
# Description:
# **************************************************************************
from flask import request
from maple.forums.models import Board
from maple.topic.models import Tags, Topic
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

    # 发表时间
    if t2 == 0:
        topic_base = Topic.query.join(Topic.board).filter(
            Topic.publish > time, Topic.is_top == False)
        if t3 == 0:
            if type == 'parent_b':
                topics = topic_base.filter(Board.parent_board == uid).paginate(
                    page, 20, True)
            elif type == 'child_b':
                topics = topic_base.filter(Board.id == uid).paginate(page, 20,
                                                                     True)
            elif type == 'tags':
                topics = Topic.query.join(Topic.tags).filter(
                    Topic.publish > time, Topic.is_top == False, Tags.tagname
                    == uid).order_by(Topic.publish.desc()).paginate(page, 20,
                                                                    True)
            else:
                topics = None
            return topics
        else:
            if type == 'parent_b':
                topics = topic_base.filter(Board.parent_board == uid).order_by(
                    Topic.publish.asc()).paginate(page, 20, True)
            elif type == 'child_b':
                topics = topic_base.filter(Board.id == uid).order_by(
                    Topic.publish.asc()).paginate(page, 20, True)
            elif type == 'tags':
                topics = Topic.query.join(Topic.tags).filter(
                    Topic.publish > time, Topic.is_top == False,
                    Tags.tagname ==
                    uid).order_by(Topic.publish.asc()).paginate(page, 20, True)
            else:
                topics = None
            return topics
    # 作者
    else:
        topic_base = Topic.query.join(Topic.board).filter(
            Topic.publish > time, Topic.is_top == False)
        if t3 == 0:
            if type == 'parent_b':
                topics = topic_base.filter(Board.parent_board == uid).order_by(
                    Topic.author_id.desc()).paginate(page, 20, True)
            elif type == 'child_b':
                topics = topic_base.filter(Board.id == uid).order_by(
                    Topic.author_id.desc()).paginate(page, 20, True)
            elif type == 'tags':
                topics = Topic.query.join(Topic.tags).filter(
                    Topic.publish > time, Topic.is_top == False, Tags.tagname
                    == uid).order_by(Topic.author_id.desc()).paginate(page, 20,
                                                                      True)
            else:
                topics = None
            return topics
        else:
            if type == 'parent_b':
                topics = topic_base.filter(Board.parent_board == uid).order_by(
                    Topic.author_id.asc()).paginate(page, 20, True)
            elif type == 'child_b':
                topics = topic_base.filter(Board.id == uid).order_by(
                    Topic.author_id.asc()).paginate(page, 20, True)
            elif type == 'tags':
                topics = Topic.query.join(Topic.tags).filter(
                    Topic.publish > time, Topic.is_top == False, Tags.tagname
                    == uid).order_by(Topic.author_id.asc()).paginate(page, 20,
                                                                     True)
            else:
                topics = None
            return topics
