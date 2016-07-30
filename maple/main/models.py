#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: models.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 13:32:12 (CST)
# Last Update:星期六 2016-7-30 12:5:38 (CST)
#          By:
# Description:
# **************************************************************************
from flask_login import current_user
from maple import redis_data
from datetime import datetime


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

    # def set_email_send():
    #     redis_data.hset('user:%s' % str(current_user.id), 'send_email_time',
    #                     datetime.utcnow())

    def get_repies_count(qid):
        pages = redis_data.hget('topic:%s' % str(qid), 'replies')
        return pages

    def get_pages(large, little):
        pages = redis_data.zscore(large, little)
        return pages


def set_email_send(uid):
    redis_data.hset('user:%s' % str(uid), 'send_email_time',
                    datetime.utcnow())
