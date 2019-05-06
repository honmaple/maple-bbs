#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: count.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-03-29 21:28:52 (CST)
# Last Update:星期日 2017-4-2 15:24:37 (CST)
#          By:
# Description: 一些统计信息
# **************************************************************************
from flask import request
from .extension import redis_data


class Count(object):
    @classmethod
    def board_topic_count(cls, pk, value=None):
        key = 'count:board:%s' % str(pk)
        if value is not None:
            pipe = redis_data.pipeline()
            pipe.hincrby(key, 'topic', value)
            pipe.execute()
        return redis_data.hget(key, 'topic') or 0

    @classmethod
    def board_post_count(cls, pk, value=None):
        key = 'count:board:%s' % str(pk)
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
        expire_key = 'expire:topic:read:{}'.format(request.remote_addr)
        if not redis_data.exists(expire_key):
            # 设置三分钟之内,阅读次数不增加
            redis_data.set(expire_key, '1')
            redis_data.expire(expire_key, 180)
            if value is not None:
                redis_data.hincrby(key, 'read', value)
        return redis_data.hget(key, 'read') or 0

    @classmethod
    def reply_liker_count(cls, replyId, value=None):
        key = 'count:reply:%s' % str(replyId)
        if value is not None:
            pipe = redis_data.pipeline()
            pipe.hincrby(key, 'liker', value)
            pipe.execute()
        return redis_data.hget(key, 'liker') or 0

    @classmethod
    def user_topic_count(cls, userId, value=None):
        key = 'count:user:%s' % str(userId)
        if value is not None:
            pipe = redis_data.pipeline()
            pipe.hincrby(key, 'topic', value)
            pipe.execute()
            cls.forums_post_count(1)
            cls.forums_topic_count(1)
        return redis_data.hget(key, 'topic') or 0

    @classmethod
    def user_reply_count(cls, userId, value=None):
        key = 'count:user:%s' % str(userId)
        if value is not None:
            pipe = redis_data.pipeline()
            pipe.hincrby(key, 'replies', value)
            pipe.execute()
            cls.forums_post_count(1)
        return redis_data.hget(key, 'replies') or 0

    @classmethod
    def user_message_count(cls, userId, value=None, clear=False):
        key = 'count:user:%s' % str(userId)
        if value is not None:
            pipe = redis_data.pipeline()
            pipe.hincrby(key, 'message', value)
            pipe.execute()
        if clear:
            redis_data.hset(key, 'message', 0)
        return redis_data.hget(key, 'message') or 0

    @classmethod
    def user_email_time(cls, userId, value=None):
        key = 'count:user:%s' % str(userId)
        if value is not None:
            redis_data.hset(key, 'email', value)
        return redis_data.hget(key, 'email') or '2015-1-1 1:1:1'

    @classmethod
    def forums_user_count(cls, value=None):
        key = 'count:forums'
        if value is not None:
            redis_data.hincrby(key, 'user', value)
        return redis_data.hget(key, 'user') or 0

    @classmethod
    def forums_topic_count(cls, value=None):
        key = 'count:forums'
        if value is not None:
            redis_data.hincrby(key, 'topic', value)
        return redis_data.hget(key, 'topic') or 0

    @classmethod
    def forums_post_count(cls, value=None):
        key = 'count:forums'
        if value is not None:
            redis_data.hincrby(key, 'post', value)
        return redis_data.hget(key, 'post') or 0
