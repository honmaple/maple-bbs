#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: count.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-03-29 21:28:52 (CST)
# Last Update:星期三 2017-3-29 22:1:2 (CST)
#          By:
# Description: 一些统计信息
# **************************************************************************
from .extension import redis_data


class Count(object):
    @classmethod
    def board_topic_count(cls, boardId, value=None):
        key = 'count:board:%s' % str(boardId)
        if value is not None:
            pipe = redis_data.pipeline()
            pipe.hincrby(key, 'topic', value)
            pipe.execute()
        return redis_data.hget(key, 'topic') or 0

    @classmethod
    def board_post_count(cls, boardId, value=None):
        key = 'count:board:%s' % str(boardId)
        if value is not None:
            pipe = redis_data.pipeline()
            pipe.hincrby(key, 'post', value)
            pipe.execute()
        return redis_data.hget(key, 'post') or 0

    @classmethod
    def topic_reply_count(cls, topicId, value=None):
        key = 'count:topic:%s' % str(topicId)
        if value is not None:
            pipe = redis_data.pipeline()
            pipe.hincrby(key, 'replies', value)
            pipe.execute()
        return redis_data.hget(key, 'replies') or 0

    @classmethod
    def topic_read_count(cls, topicId, value=None):
        key = 'count:topic:%s' % str(topicId)
        if value is not None:
            pipe = redis_data.pipeline()
            pipe.hincrby(key, 'read', value)
            pipe.execute()
        return redis_data.hget(key, 'read') or 0

    @classmethod
    def user_topic_count(cls, userId, value=None):
        key = 'count:user:%s' % str(userId)
        if value is not None:
            pipe = redis_data.pipeline()
            pipe.hincrby(key, 'topic', value)
            pipe.execute()
        return redis_data.hget(key, 'topic') or 0

    @classmethod
    def user_reply_count(cls, userId, value=None):
        key = 'count:user:%s' % str(userId)
        if value is not None:
            pipe = redis_data.pipeline()
            pipe.hincrby(key, 'replies', value)
            pipe.execute()
        return redis_data.hget(key, 'replies') or 0
