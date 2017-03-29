#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-03-28 16:15:08 (CST)
# Last Update:星期三 2017-3-29 19:1:59 (CST)
#          By:
# Description:
# **************************************************************************
from flask import redirect, render_template, request, url_for
from flask_babelex import gettext as _
from flask_login import current_user

from flask_maple.auth.forms import form_validate
from flask_maple.response import HTTPResponse
from forums.api.forms import (CollectForm, ReplyForm, TopicForm,
                              collect_error_callback, error_callback,
                              form_board)
from forums.api.forums.models import Board
from forums.api.tag.models import Tags
from forums.api.topic.models import Topic
from forums.common.serializer import Serializer
from forums.common.utils import gen_filter_dict, gen_order_by
from forums.common.views import IsAuthMethodView as MethodView

from .models import Collect


class CollectListView(MethodView):
    def get(self):
        query_dict = request.data
        user = request.user
        form = CollectForm()
        page, number = self.page_info
        keys = ['name']
        order_by = gen_order_by(query_dict, keys)
        filter_dict = gen_filter_dict(query_dict, keys)
        filter_dict.update(author_id=user.id)
        collects = Collect.query.filter_by(
            **filter_dict).order_by(*order_by).paginate(page, number, True)
        data = {'title': 'Collect', 'collects': collects, 'form': form}
        return render_template('collect/collect_list.html', **data)

    @form_validate(CollectForm, error=collect_error_callback, f='')
    def post(self):
        user = request.user
        form = CollectForm()
        name = form.name.data
        description = form.description.data
        is_hidden = form.is_hidden.data
        is_hidden = True if is_hidden == 0 else False
        collect = Collect(
            name=name, description=description, is_hidden=is_hidden)
        collect.author = user
        collect.save()
        return redirect(url_for('collect.list'))


class CollectView(MethodView):
    def get(self, pk):
        user = request.user
        page, number = self.page_info
        collect = Collect.query.filter_by(
            id=pk, author_id=user.id).first_or_404()
        form = CollectForm()
        form.name.data = collect.name
        form.description.data = collect.description
        form.is_hidden.data = 0 if collect.is_hidden else 1
        topics = collect.topics.paginate(page, number, True)
        data = {'collect': collect, 'topics': topics, 'form': form}
        return render_template('collect/collect.html', **data)

    def put(self, pk):
        post_data = request.data
        collect = Collect.query.filter_by(id=pk).first_or_404()
        name = post_data.pop('name', None)
        description = post_data.pop('description', None)
        is_hidden = post_data.pop('is_hidden', None)
        if name is not None:
            collect.name = name
        if description is not None:
            collect.description = description
        if is_hidden is not None:
            collect.is_hidden = is_hidden
        collect.save()
        return HTTPResponse(HTTPResponse.NORMAL_STATUS).to_response()

    def delete(self, pk):
        collect = Collect.query.filter_by(id=pk).first_or_404
        collect.delete()
        return HTTPResponse(HTTPResponse.NORMAL_STATUS).to_response()


class AddToCollectView(MethodView):
    def post(self, topicId):
        user = request.user
        form = request.form.getlist('add-to-collect')
        topic = Topic.query.filter_by(id=topicId).first_or_404()
        for cid in form:
            '''This has a problem'''
            collect = Collect.query.filter_by(id=cid).first_or_404()
            if not Collect.query.filter_by(
                    topics__id=topic.id, author_id=user.id).exists():
                collect.topics.append(topic)
                collect.save()
        return redirect(url_for('topic.topic', topicId=topic.id))

    # def delete(self, topicId):
    #     user = request.user
    #     form = request.form.getlist('add-to-collect')
    #     topic = Topic.query.filter_by(id=topicId).first_or_404()
    #     for cid in form:
    #         '''This has a problem'''
    #         collect = Collect.query.filter_by(id=cid).first_or_404()
    #         if not Collect.query.filter_by(
    #                 topics__id=topic.id, author_id=user.id).exists():
    #             collect.topics.append(topic)
    #             collect.save()
    #     return redirect(url_for('topic.topic', topicId=topic.id))
