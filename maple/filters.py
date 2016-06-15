#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: filter.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-06-15 00:39:29 (CST)
# Last Update:星期三 2016-6-15 18:44:9 (CST)
#          By:
# Description:
# **************************************************************************
from datetime import datetime
from maple import redis_data
from maple.settings import setting
from maple.topic.models import Reply, Topic
from maple.user.models import User


class Filters(object):
    def timesince(dt, default="just now"):
        now = datetime.now()
        diff = now - dt
        if diff.days > 10:
            return dt.strftime('%Y-%m-%d %H:%M')
        if diff.days <= 10 and diff.days > 0:
            periods = ((diff.days, "day", "days"), )
        if diff.days <= 0 and diff.seconds > 3600:
            periods = ((diff.seconds / 3600, "hour", "hours"), )
        if diff.seconds <= 3600 and diff.seconds > 90:
            periods = ((diff.seconds / 60, "minute", "minutes"), )
        if diff.seconds <= 90:
            return default

        # periods = ((diff.days / 365, "year", "years"),
        #            (diff.days / 30, "month", "months"),
        #            (diff.days / 7, "week", "weeks"),
        #            (diff.days, "day", "days"),
        #            (diff.seconds / 3600, "hour", "hours"),
        #            (diff.seconds / 60, "minute", "minutes"),
        #            (diff.seconds, "second", "seconds"), )

        for period, singular, plural in periods:

            if period:
                return "%d %s ago" % (period, singular if period == 1 else
                                      plural)

        return default

    def get_last_reply(uid):
        reply = Reply.query.join(Reply.topic).filter(Topic.id == uid).first()
        return reply

    def get_user_infor(name):
        user = User.query.filter(User.username == name).first()
        return user

    def get_read_count(id):
        read = redis_data.hget('topic:%s' % str(id), 'read')
        replies = redis_data.hget('topic:%s' % str(id), 'replies')
        if not read:
            read = 0
        else:
            read = int(read)
        if not replies:
            replies = 0
        else:
            replies = int(replies)
        return replies, read

    class Title(object):
        title = setting['title']
        picture = setting['picture']
        description = setting['description']
