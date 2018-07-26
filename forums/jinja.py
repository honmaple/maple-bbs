#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: jinja.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-11-07 21:00:32 (CST)
# Last Update: Thursday 2018-07-26 09:54:53 (CST)
#          By:
# Description:
# **************************************************************************
from datetime import datetime
from config import SITE

from bleach import clean
from flask import Markup, g
from flask_babel import format_datetime
from misaka import HtmlRenderer, Markdown


def safe_clean(text):
    tags = ['b', 'i', 'font', 'br', 'blockquote', 'div', 'h2', 'a', 'p']
    attrs = {'*': ['style', 'id', 'class'], 'font': ['color'], 'a': ['href']}
    styles = ['color']
    return Markup(clean(text, tags=tags, attributes=attrs, styles=styles))


def markdown(text, clean=True):
    renderer = HtmlRenderer()
    md = Markdown(renderer, extensions=('fenced-code', ))
    if clean:
        return Markup(safe_clean(md(text)))
    return Markup(md(text))


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
    if g.user.is_authenticated:
        return 'LOCALE:' + format_datetime(datetime.utcnow())
    return 'UTC:' + format_datetime(datetime.utcnow())


def hot_tags():
    from forums.api.tag.models import Tags
    tags = Tags.query.limit(9).all()
    return tags


def recent_tags():
    from forums.api.tag.models import Tags
    tags = Tags.query.limit(12).all()
    return tags


def forums_count():
    from forums.extension import redis_data
    key = 'count:forums'
    return redis_data.hgetall(key)


def init_app(app):

    app.jinja_env.globals['SITE'] = SITE
    app.jinja_env.globals['hot_tags'] = hot_tags
    app.jinja_env.globals['recent_tags'] = recent_tags
    app.jinja_env.globals['show_time'] = show_time
    app.jinja_env.globals['forums_count'] = forums_count
    app.jinja_env.filters['timesince'] = timesince
    app.jinja_env.filters['safe_clean'] = safe_clean
