#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: records.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-06-04 19:57:49 (CST)
# Last Update:星期二 2016-8-2 21:58:28 (CST)
#          By:
# Description:
# **************************************************************************
from time import time
from datetime import datetime
from maple import redis_data
from flask import current_app, g


def mark_online(user_ip):
    config = current_app.config
    now_time = int(time()) + 28800
    expires = config.get('ONLINE_LAST_MINUTES', 5) * 60
    online_users = 'online_users:%d' % (now_time // 60)
    active_users = 'active_users:%s' % user_ip
    pipe = redis_data.pipeline()
    if g.user.is_authenticated:
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


def load_online_users(mode):
    if mode == 1:
        online_users = load_online_all_users()
        high_online = redis_data.hget('online_users', 'high:counts')
        count = len(online_users)
        if int(high_online) < count:
            redis_data.hset('online_users', 'high:counts', count)
            redis_data.hset('online_users', 'high:time', int(time()) + 28800)
        return count
    if mode == 2:
        # 'online sign users'
        online_users = load_online_sign_users()
        return len(online_users)
    if mode == 3:
        # 'guest users'
        online_users = load_online_all_users()
        online_sign_users = load_online_sign_users()
        return len(online_users) - len(online_sign_users)
    if mode == 4:
        counts = redis_data.hget('online_users', 'high:counts')
        return counts
    if mode == 5:
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
