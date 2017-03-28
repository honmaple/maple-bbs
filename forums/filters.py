#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: filters.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-11-07 21:00:32 (CST)
# Last Update:星期二 2017-3-28 21:12:1 (CST)
#          By:
# Description:
# **************************************************************************
from datetime import datetime

from bleach import clean
from flask import Markup, g
from flask_babelex import format_datetime
from flask_login import current_user
from misaka import HtmlRenderer, Markdown

from forums.api.topic.models import Reply, Topic
from forums.api.user.models import User
from forums.extension import redis_data


def safe_clean(text):
    tags = ['b', 'i', 'font', 'br', 'blockquote', 'div', 'h2', 'a']
    attrs = {'*': ['style', 'id', 'class'], 'font': ['color'], 'a': ['href']}
    styles = ['color']
    return Markup(clean(text, tags=tags, attributes=attrs, styles=styles))


def markdown(text):
    renderer = HtmlRenderer()
    md = Markdown(renderer, extensions=('fenced-code', ))
    return Markup(md(text))


def safe_markdown(text):
    renderer = HtmlRenderer()
    md = Markdown(renderer, extensions=('fenced-code', ))
    return Markup(safe_clean(md(text)))


def timesince(dt, default="just now"):
    now = datetime.utcnow()
    diff = now - dt
    if diff.days > 10:
        return format_datetime(dt, 'Y-M-d H:m')
    elif diff.days <= 10 and diff.days > 0:
        periods = ((diff.days, "day", "days"), )
    elif diff.days <= 0 and diff.seconds > 3600:
        periods = ((diff.seconds / 3600, "hour", "hours"), )
    elif diff.seconds <= 3600 and diff.seconds > 90:
        periods = ((diff.seconds / 60, "minute", "minutes"), )
    else:
        return default

    for period, singular, plural in periods:

        if period:
            return "%d %s ago" % (period, singular if period == 1 else plural)

    return default


def show_time():
    from flask_babelex import format_datetime
    if g.user.is_authenticated:
        return 'LOCALE:' + format_datetime(datetime.utcnow())
    else:
        return 'UTC:' + format_datetime(datetime.utcnow())


def get_user_infor(name):
    user = User.query.filter(User.username == name).first()
    return user


def get_last_reply(uid):
    reply = Reply.query.join(Reply.topic).filter(Topic.id == uid).first()
    return reply


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


def notice_count():
    from forums.api.forums.models import Notice
    if g.user.is_authenticated:
        count = Notice.query.filter_by(
            rece_id=g.user.id, is_read=False).count()
        if count > 0:
            return count
    return None


def hot_tags():
    from forums.api.tag.models import Tags
    tags = Tags.query.limit(9).all()
    return tags


def recent_tags():
    from forums.api.tag.models import Tags
    tags = Tags.query.limit(12).all()
    return tags


def is_liked(replyId):
    from forums.api.topic.models import Reply
    return Reply.query.filter_by(
        likers__id=current_user.id, id=replyId).exists()


def topic_is_followed(topicId):
    from forums.api.topic.models import Topic
    return Topic.query.filter_by(
        followers__id=current_user.id, id=topicId).exists()


def tag_is_followed(pk):
    from forums.api.tag.models import Tags
    return Tags.query.filter_by(followers__id=current_user.id, id=pk).exists()


def user_is_followed(pk):
    from forums.api.user.models import User
    return User.query.filter_by(followers__id=current_user.id, id=pk).exists()


def is_collected(topicId):
    from forums.api.collect.models import Collect
    return Collect.query.filter_by(
        topics__id=topicId, author_id=current_user.id).exists()


def is_online(username):
    from forums.common.records import load_online_sign_users
    online_users = load_online_sign_users()
    if username in online_users:
        return True
    return False


class Title(object):
    setting = {'title': 'Honmaple', 'picture': '', 'description': '爱生活，更爱自由'}
    title = setting['title']
    picture = setting['picture']
    description = setting['description']


def register_jinja2(app):

    app.jinja_env.globals['Title'] = Title
    app.jinja_env.globals['hot_tags'] = hot_tags
    app.jinja_env.globals['recent_tags'] = recent_tags
    app.jinja_env.globals['notice_count'] = notice_count
    app.jinja_env.globals['show_time'] = show_time
    app.jinja_env.filters['get_last_reply'] = get_last_reply
    app.jinja_env.filters['get_user_infor'] = get_user_infor
    app.jinja_env.filters['get_read_count'] = get_read_count
    app.jinja_env.filters['timesince'] = timesince
    app.jinja_env.filters['markdown'] = safe_markdown
    app.jinja_env.filters['safe_clean'] = safe_clean
    app.jinja_env.filters['is_collected'] = is_collected
    app.jinja_env.filters['is_online'] = is_online
    app.jinja_env.filters['is_liked'] = is_liked
    app.jinja_env.filters['topic_is_followed'] = topic_is_followed
    app.jinja_env.filters['tag_is_followed'] = tag_is_followed
    app.jinja_env.filters['user_is_followed'] = tag_is_followed
