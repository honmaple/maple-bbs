#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: models.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 13:32:12 (CST)
# Last Update:星期二 2016-6-14 23:20:15 (CST)
#          By:
# Description:
# **************************************************************************
from maple import redis_data, db
from maple.helpers import make_uid
from maple.topic.models import Topic, Tags, Reply
from flask_login import current_user
from re import split as sp


class RedisData(object):
    def set_topics():
        '''使用redis记录'''
        pipe = redis_data.pipeline()
        '''用户发帖数'''
        user = 'user:%s' % str(current_user.id)
        pipe.hincrby(user, 'topic', 1)
        pipe.hincrby(user, 'all:topic', 1)
        pipe.execute()

    def set_replies(qid):
        pipe = redis_data.pipeline()
        pipe.hincrby('topic:%s' % str(qid), 'replies', 1)
        pipe.execute()

    def set_read_count(qid):
        redis_data.hincrby('topic:%s' % str(qid), 'read', 1)

    def set_notice(user):
        redis_data.hincrby('user:%s' % str(user.id), 'notice', 1)

    def set_collect(user, num):
        redis_data.hincrby('user:%s' % str(user.id), 'collect', num)

    def set_love(user, num):
        redis_data.hincrby('user:%s' % str(user.id), 'love', num)

    def set_user():
        redis_data.hincrby('user:%s' % str(current_user.id), 'topic', 1)

    def set_user_all():
        redis_data.hincrby('user:%s' % str(current_user.id), 'all_topic', 1)

    def get_repies_count(qid):
        pages = redis_data.hget('topic:%s' % str(qid), 'replies')
        return pages

    def get_pages(large, little):
        pages = redis_data.zscore(large, little)
        return pages


class SQLData(object):
    def set_topics(form):
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
                exsit_tag = Tags.query.filter_by(tagname = tag).first()
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

    def set_replies(form, uid):
        reply = Reply()
        reply.content = form.content.data
        reply.author = current_user
        reply.topic_id = uid
        db.session.add(reply)
        db.session.commit()
        reply.topic.board.count.all_topics += 1
        db.session.commit()
        RedisData.set_replies(uid)
