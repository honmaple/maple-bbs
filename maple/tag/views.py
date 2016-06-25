#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 13:18:19 (CST)
# Last Update:星期六 2016-6-25 17:59:5 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint, render_template, request, url_for
from maple import app
from maple.helpers import is_num
from maple.topic.models import Tags, Topic
from maple.filters import Filters
from urllib.parse import urljoin
from werkzeug.utils import escape
from werkzeug.contrib.atom import AtomFeed

site = Blueprint('tag', __name__)


@site.route('', defaults={'tag': None})
@site.route('/<tag>')
def tag(tag):
    if tag is None:
        tags = Tags.query.distinct(Tags.tagname).all()
        data = {'tags': tags}
        return render_template('forums/tag_list.html', **data)
    else:
        page = is_num(request.args.get('page'))
        topic_base = Topic.query.join(Topic.tags).filter(Tags.tagname == tag)
        topics = topic_base.filter(Topic.is_top == False).paginate(
            page, app.config['PER_PAGE'],
            error_out=True)
        top_topics = topic_base.filter(Topic.is_top == True).limit(5).all()
        tag = Tags.query.filter_by(tagname=tag).first_or_404()
        data = {'tag': tag, 'topics': topics, 'top_topics': top_topics}
        return render_template('forums/tag.html', **data)


@site.route('/<tag>/feed')
def rss(tag):
    feed = AtomFeed('%s·HonMaple社区' % tag,
                    feed_url=request.url,
                    url=request.url_root,
                    subtitle='I like solitude, yearning for freedom')
    topics = Topic.query.join(Topic.tags).filter(Tags.tagname == tag).limit(
        10).all()
    for topic in topics:
        feed.add(
            topic.title,
            escape(Filters.safe_markdown(topic.content) if topic.is_markdown
                   else topic.content),
            content_type='html',
            author=topic.author.username,
            url=urljoin(request.url_root,
                        url_for('topic.topic', uid=topic.uid)),
            updated=topic.publish,
            published=topic.publish)
    return feed.get_response()
