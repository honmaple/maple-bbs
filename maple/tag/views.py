#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 13:18:19 (CST)
# Last Update:星期日 2016-11-6 10:9:52 (CST)
#          By:
# Description:
# **************************************************************************
from flask import render_template, request, url_for, current_app
from flask.views import MethodView
from flask_babelex import gettext as _
from maple.topic.models import Topic
from maple.filters import Filters
from .models import Tags
from urllib.parse import urljoin
from werkzeug.utils import escape
from werkzeug.contrib.atom import AtomFeed


class TagListView(MethodView):
    def get(self):
        tags = Tags.query.distinct(Tags.tagname).all()
        data = {'title': _('All Tags - '), 'tags': tags}
        return render_template('tag/tag_list.html', **data)


class TagView(MethodView):
    def get(self, tag):
        page = request.args.get('page', 1, type=int)
        topic_base = Topic.query.join(Topic.tags).filter(Tags.tagname == tag)
        topics = topic_base.filter(Topic.is_top == False).paginate(
            page, current_app.config['PER_PAGE'], error_out=True)
        top_topics = topic_base.filter(Topic.is_top == True).limit(5).all()
        tag = Tags.query.filter_by(tagname=tag).first_or_404()
        data = {
            'title': '%s - ' % tag,
            'tag': tag,
            'topics': topics,
            'top_topics': top_topics
        }
        return render_template('tag/tag.html', **data)


class TagRssView(MethodView):
    def get(self, tag):
        feed = AtomFeed(
            '%s·HonMaple社区' % tag,
            feed_url=request.url,
            url=request.url_root,
            subtitle='I like solitude, yearning for freedom')
        topics = Topic.query.join(Topic.tags).filter(
            Tags.tagname == tag).limit(10).all()
        for topic in topics:
            feed.add(topic.title,
                     escape(
                         Filters.safe_markdown(topic.content)
                         if topic.is_markdown else topic.content),
                     content_type='html',
                     author=topic.author.username,
                     url=urljoin(
                         request.url_root,
                         url_for(
                             'topic.topic', topicId=topic.uid)),
                     updated=topic.publish,
                     published=topic.publish)
        return feed.get_response()
