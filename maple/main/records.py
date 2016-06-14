#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: records.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-06-04 19:57:49 (CST)
# Last Update:星期二 2016-6-14 23:20:15 (CST)
#          By:
# Description:
# **************************************************************************
from time import time
from datetime import datetime
from maple import redis_data
from flask import current_app, g


def mark_online(user_ip):
    '''记录在线用户'''
    pipe = redis_data.pipeline()
    config = current_app.config
    now_time = int(time()) + 28800
    expires = config['ONLINE_LAST_MINUTES'] * 60
    '''分钟'''
    online_users = 'online_users:%d' % (now_time // 60)
    active_users = 'active_users:%s' % user_ip
    '''注册用户'''
    if g.user is not None and g.user.is_authenticated:
        online_sign_users = 'online_sign_users:%d' % (now_time // 60)
        active_sign_users = 'active_sign_users:%s' % user_ip
        pipe.sadd(online_sign_users, user_ip)
        pipe.set(active_sign_users, now_time)
        pipe.expire(online_sign_users, expires)
        pipe.expire(active_sign_users, expires)
    pipe.sadd(online_users, user_ip)
    pipe.set(active_users, now_time)
    pipe.expire(online_users, expires)
    pipe.expire(active_users, expires)

    high = redis_data.hget('online_users', 'high:counts')
    if not high:
        pipe.hset('online_users', 'high:counts', 1)
    high_time = redis_data.hget('online_users', 'high:time')
    if not high_time:
        pipe.hset('online_users', 'high:time', now_time)
    pipe.execute()

# def load_user_last_activity(user_ip):
# last_active = redis_data.get('active_users:%s' % user_ip)
# if last_active is None:
# last_active = time() + 28800
# return datetime.utcfromtimestamp(int(last_active))


def load_online_users(mode):
    if mode == 'counts':
        counts = len(load_online_all_users()) - len(load_online_sign_users())
        return counts
    if mode == 'all_counts':
        counts = len(load_online_all_users())
        high = redis_data.hget('online_users', 'high:counts')
        if counts > int(high):
            redis_data.hset('online_users', 'high:counts', counts)
            redis_data.hset('online_users', 'high:time', int(time()) + 28800)
        return counts
    if mode == 'sign_counts':
        return len(load_online_sign_users())
    if mode == 'high':
        counts = redis_data.hget('online_users', 'high:counts')
        return int(counts)
    if mode == 'high_time':
        high_time = redis_data.hget('online_users', 'high:time')
        return datetime.utcfromtimestamp(int(high_time))


def load_online_all_users():
    config = current_app.config
    current = (int(time()) + 28800) // 60
    minutes = range(config['ONLINE_LAST_MINUTES'])
    return redis_data.sunion(['online_users:%d' % (current - x) for x in
                              minutes])


def load_online_sign_users():
    config = current_app.config
    current = (int(time()) + 28800) // 60
    minutes = range(config['ONLINE_LAST_MINUTES'])
    return redis_data.sunion(['online_sign_users:%d' % (current - x)
                              for x in minutes])
