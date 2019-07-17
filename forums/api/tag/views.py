#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-15 22:07:04 (CST)
# Last Update: Wednesday 2019-05-08 16:27:50 (CST)
#          By:
# Description:
# **************************************************************************
from urllib.parse import urljoin

from flask import current_app, render_template, request, url_for
from werkzeug.contrib.atom import AtomFeed

from forums.api.topic.db import Topic
from forums.api.utils import gen_topic_filter, gen_topic_orderby
from forums.common.views import BaseMethodView as MethodView
from forums.utils import filter_maybe, orderby_maybe
from forums.default import SITE

from .db import Tags


class TagsListView(MethodView):
    per_page = 99

    def get(self):
        request_data = request.data
        page, number = self.pageinfo
        params = filter_maybe(request_data, ["name"])
        orderby = orderby_maybe(request_data, ["name"])
        tags = Tags.query.filter_by(**params).order_by(*orderby).paginate(
            page, number, True)
        data = {'tags': tags}
        return render_template('tag/tag_list.html', **data)


class TagsView(MethodView):
    def get(self, name):
        request_data = request.data
        page, number = self.pageinfo
        tag = Tags.query.filter_by(name=name).first_or_404()

        keys = ['name']
        params = gen_topic_filter(request_data, keys)
        params.update(tags__id=tag.id)
        orderby = gen_topic_orderby(request_data, keys)
        topics = Topic.query.filter_by(**params).order_by(*orderby).paginate(
            page, number, True)

        data = {'tag': tag, 'topics': topics}
        return render_template('tag/tag.html', **data)


class TagFeedView(MethodView):
    def get(self, name):
        title = SITE['title']
        subtitle = SITE['subtitle']
        feed = AtomFeed(
            '%s·%s' % (name, title),
            feed_url=request.url,
            url=request.url_root,
            subtitle=subtitle)
        topics = Topic.query.filter_by(tags__name=name).limit(10)
        for topic in topics:
            feed.add(
                topic.title,
                topic.text,
                content_type='html',
                author=topic.author.username,
                url=urljoin(request.url_root,
                            url_for('topic.topic', pk=topic.id)),
                updated=topic.updated_at,
                published=topic.created_at)
        return feed.get_response()
