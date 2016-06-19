#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: filter.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-06-15 00:39:29 (CST)
# Last Update:星期日 2016-6-19 16:26:44 (CST)
#          By:
# Description:
# **************************************************************************
from datetime import datetime
from maple import redis_data
from maple.settings import setting
from maple.topic.models import Reply, Topic
from maple.user.models import User
from flask import Markup
from misaka import Markdown, HtmlRenderer
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from bleach import clean


def safe_clean(text):
    tags = ['b', 'i', 'font', 'br', 'blockquote', 'div', 'h2']
    attrs = {'*': ['style', 'id', 'class'], 'font': ['color']}
    styles = ['color']
    return Markup(clean(text, tags=tags, attributes=attrs, styles=styles))


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
