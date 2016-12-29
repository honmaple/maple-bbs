#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: filters.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-11-07 21:00:32 (CST)
# Last Update:星期日 2016-12-18 18:6:38 (CST)
#          By:
# Description:
# **************************************************************************
from datetime import datetime
from maple.extension import redis_data, cache
from maple.settings import setting
from api.topic.models import Topic
from api.reply.models import Reply
from api.user.models import User
from flask import Markup, g
from misaka import Markdown, HtmlRenderer
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from bleach import clean


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
    from flask_babelex import format_datetime
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


class Filters(object):
    def safe_markdown(text):
        class HighlighterRenderer(HtmlRenderer):
            def blockcode(self, text, lang):
                lang = 'python'
                if not lang:
                    return '\n<pre><code>{}</code></pre>\n'.format(text.strip(
                    ))
                lexer = get_lexer_by_name(lang, stripall=True)
                formatter = HtmlFormatter()
                return highlight(text, lexer, formatter)

        renderer = HighlighterRenderer()
        md = Markdown(renderer, extensions=('fenced-code', ))
        return Markup(md(safe_clean(text)))
        # return Markup(md(text))

    def timesince(dt, default="just now"):
        from flask_babelex import format_datetime
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
                return "%d %s ago" % (period, singular
                                      if period == 1 else plural)

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

    @cache.memoize(timeout=60)
    def get_last_reply(uid):
        reply = Reply.query.join(Reply.topic).filter(Topic.id == uid).first()
        return reply

    @cache.memoize(timeout=30)
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

    @cache.memoize(timeout=30)
    def is_collected(topicId):
        from maple.topic.models import CollectTopic
        from flask_login import current_user
        for collect in current_user.collects:
            cid = CollectTopic.query.filter_by(
                collect_id=collect.id, topic_id=topicId).first()
            if cid is not None:
                return True
        return False

    def notice_count():
        from maple.forums.models import Notice
        if g.user.is_authenticated:
            count = Notice.query.filter_by(
                rece_id=g.user.id, is_read=False).count()
            if count > 0:
                return count
        return None

    @cache.memoize(timeout=60)
    def hot_tags():
        from api.tag.models import Tags
        tags = Tags.query.limit(9).all()
        return tags

    @cache.memoize(timeout=60)
    def recent_tags():
        from api.tag.models import Tags
        tags = Tags.query.limit(12).all()
        return tags

    def is_online(username):
        from maple.main.records import load_online_sign_users
        online_users = load_online_sign_users()
        if username in online_users:
            return True
        return False

    class Title(object):
        title = setting['title']
        picture = setting['picture']
        description = setting['description']


def register_jinja2(app):

    app.jinja_env.globals['Title'] = Filters.Title
    app.jinja_env.globals['hot_tags'] = Filters.hot_tags
    app.jinja_env.globals['recent_tags'] = Filters.recent_tags
    app.jinja_env.globals['notice_count'] = Filters.notice_count
    app.jinja_env.globals['show_time'] = Filters.show_time
    app.jinja_env.filters['get_last_reply'] = Filters.get_last_reply
    app.jinja_env.filters['get_user_infor'] = Filters.get_user_infor
    app.jinja_env.filters['get_read_count'] = Filters.get_read_count
    app.jinja_env.filters['timesince'] = Filters.timesince
    app.jinja_env.filters['markdown'] = Filters.safe_markdown
    app.jinja_env.filters['safe_clean'] = safe_clean
    app.jinja_env.filters['is_collected'] = Filters.is_collected
    app.jinja_env.filters['is_online'] = Filters.is_online
