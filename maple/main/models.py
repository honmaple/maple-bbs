#!/usr/bin/env python
# -*- coding=UTF-8 -*-
#*************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: redis_db.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2016-03-12 19:43:41
#*************************************************************************
from maple import redis_data
from flask_login import current_user


class RedisData(object):

    def set_question():
        '''使用redis记录'''
        pipe = redis_data.pipeline()
        '''用户发帖数'''
        user = 'user:%s' % str(current_user.id)
        pipe.hincrby(user, 'topic', 1)
        pipe.hincrby(user, 'all:topic', 1)
        pipe.execute()

    def set_replies(qid):
        pipe = redis_data.pipeline()
        pipe.hincrby('question:%s' % str(qid), 'replies', 1)
        pipe.execute()

    def set_read_count(qid):
        redis_data.hincrby('question:%s' % str(qid), 'read', 1)

    def set_notice(user):
        redis_data.hincrby('user:%s' % str(user.id), 'notice', 1)

    def set_collect(user,num):
        redis_data.hincrby('user:%s' % str(user.id), 'collect', num)

    def set_love(user,num):
        redis_data.hincrby('user:%s' % str(user.id), 'love', num)

    def set_user():
        redis_data.hincrby('user:%s' % str(current_user.id), 'topic', 1)

    def set_user_all():
        redis_data.hincrby('user:%s' % str(current_user.id), 'all_topic', 1)

    def get_repies_count(qid):
        pages = redis_data.hget('question:%s' % str(qid), 'replies')
        return pages

    def get_pages(large, little):
        pages = redis_data.zscore(large, little)
        return pages
