#*************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: jinja2_filter.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2016-02-16 21:38:02
#*************************************************************************
#!/usr/bin/env python
# -*- coding=UTF-8 -*-
from maple import redis_data
from flask_login import current_user

def join_time(uid,gid):
    from maple.group.models import UserGroup
    return UserGroup.load_join_time(uid,gid).join_time

def groups(kind):
    from maple.group.models import Group
    return Group.load_by_kind(kind)

def safe_clean(text):
    from flask import Markup
    from bleach import clean
    tags = ['b','i','font','br','blockquote']
    attrs = {
        '*':['style'],
        'font':['color']
    }
    styles = ['color']
    return Markup(clean(text,tags = tags,
                        attributes = attrs,
                        styles = styles))

def safe_markdown(text):
    from flask import Markup
    from misaka import Markdown, HtmlRenderer
    html = HtmlRenderer()
    markdown = Markdown(html)
    return Markup(markdown(text))

def judge(id,mode):
    if mode == 'collect':
        from maple.question.models import Collector
        collect = Collector.load_by_id(id,current_user.id)
        if collect:
            return True
        else:
            return False
    if mode == 'love':
        from maple.question.models import Lover
        lover = Lover.load_by_id(id,current_user.id)
        if lover:
            return True
        else:
            return False
    if mode == 'daily':
        user = 'user' + ':' +  'daily' + ':' + str(id)
        if redis_data.exists(user):
            return True
        else:
            return False
    if mode == 'notice':
        user = 'user' + ':' + str(id)
        notice = redis_data.hget(user,'notice')
        if not notice:
            notice = 0
        else:
            notice = int(notice)
        return notice

def load_read_count(id):
    read = redis_data.hget('question:%s'%str(id),'read')
    replies = redis_data.hget('question:%s'%str(id),'replies')
    if not read:
        read = 0
    else:
        read = int(read)
    if not replies:
        replies = 0
    else:
        replies = int(replies)
    return replies,read

def load_user_count(id):
    topic = redis_data.hget('user:%s'%str(current_user.id),'topic')
    all_topic = redis_data.hget('user:%s'%str(current_user.id),'all_topic')
    collect = redis_data.hget('user:%s'%str(current_user.id),'collect')
    if not topic:
        topic = 0
    else:
        topic = int(topic)
    if not all_topic:
        all_topic = 0
    else:
        all_topic = int(all_topic)
    if not collect:
        collect = 0
    else:
        collect = int(collect)
    return topic,all_topic,collect

def load_forums_count(id):
    topic = redis_data.hget('forums:count','topic')
    group = redis_data.hget('forums:count','group')
    user = redis_data.hget('forums:count','user')
    if not topic:
        topic = 0
    else:
        topic = int(topic)
    if not group:
        group = 0
    else:
        group = int(group)
    if not user:
        user = 0
    else:
        user = int(user)
    return topic,group,user


