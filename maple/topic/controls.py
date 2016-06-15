#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: controls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-06-15 10:22:42 (CST)
# Last Update:星期三 2016-6-15 14:7:48 (CST)
#          By:
# Description:
# **************************************************************************
from flask_login import current_user
from maple import db
from maple.helpers import make_uid
from maple.main.models import RedisData
from .models import Topic, Tags, Reply
from re import split as sp


class TopicModel(object):
    def post_data(form):
        topic = Topic()
        topic.title = form.title.data
        topic.content = form.content.data
        topic.uid = make_uid()
        topic.author = current_user
        tags = sp(',|;|，|；| ', form.tags.data)
        tags = list(set(tags))[:4]
        post_tags = []
        for tag in tags:
            if tag != '':
                exsit_tag = Tags.query.filter_by(tagname=tag).first()
                if exsit_tag is not None:
                    post_tags.append(exsit_tag)
                else:
                    t = Tags()
                    t.tagname = tag
                    post_tags.append(t)
        topic.tags = post_tags
        topic.board_id = form.category.data
        db.session.add(topic)
        db.session.commit()
        topic.board.count.topics += 1
        topic.board.count.all_topics += 1
        db.session.commit()
        RedisData.set_topics()
        return topic


class ReplyModel(object):
    def post_data(form, uid):
        reply = Reply()
        reply.content = form.content.data
        reply.author = current_user
        reply.topic_id = uid
        db.session.add(reply)
        db.session.commit()
        reply.topic.board.count.all_topics += 1
        db.session.commit()
        RedisData.set_replies(uid)
