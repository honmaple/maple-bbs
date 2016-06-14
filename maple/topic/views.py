#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 13:47:04 (CST)
# Last Update:星期二 2016-6-14 23:20:13 (CST)
#          By:
# Description:
# **************************************************************************
from flask import (Blueprint, render_template, redirect, url_for, request)
from flask.views import MethodView
from flask_login import login_required
from flask_maple.forms import flash_errors
from maple import app
from maple.main.models import SQLData, RedisData
from maple.main.permission import topic_permission, reply_permission
from maple.helpers import is_num
from maple.forums.models import Board
from maple.topic.models import Topic
from maple.topic.forms import TopicForm, ReplyForm

site = Blueprint('topic', __name__)


@site.route('/ask')
@login_required
def ask():
    form = TopicForm()
    boardId = request.args.get('boardId')
    if boardId is not None:
        board = Board.query.filter_by(id=boardId).first()
        form.category.data = board.id
    return render_template('topic/ask.html', form=form)

# @site.route('/topic/<uid>/edit', methods=['POST'])
# def edit(uid):
#     topic = Topic.query.filter_by(uid=uid).first_or_404()
#     form = TopicForm()
#     form.title.data = topic.title
#     tags = ''
#     leng = 1
#     for tag in topic.tags:
#         if leng == len(list(topic.tags)):
#             tags += tag.tagname
#         else:
#             tags += tag.tagname + ','
#         leng += 1
#     form.tags.data = tags
#     form.content.data = topic.content
#     return jsonify(form=form)
#     # return render_template('topic/edit.html', form=form)


class TopicAPI(MethodView):
    decorators = [topic_permission]

    def template_with_uid(self, form, topic, replies):
        data = {'topic': topic, 'replies': replies, 'form': form}
        return render_template('topic/content.html', **data)

    def template_without_uid(self, topics):
        return render_template('topic/topic.html', topics=topics)

    def get(self, uid):
        page = is_num(request.args.get('page'))
        if uid is None:
            topics = Topic.query.paginate(page,
                                          app.config['PER_PAGE'],
                                          error_out=True)
            return self.template_without_uid(topics)
        else:
            form = ReplyForm()
            topic = Topic.query.filter_by(uid=str(uid)).first_or_404()
            replies = topic.replies.paginate(page, 5, True)
            RedisData.set_read_count(topic.id)
            return self.template_with_uid(form, topic, replies)

    def post(self):
        form = TopicForm()
        if form.validate_on_submit():
            SQLData.set_topics(form)
            return redirect('/')
        else:
            if form.errors:
                flash_errors(form)
                form.title.data = form.title.data
            else:
                pass
            form.title.data = form.title.data
            return redirect(url_for('topic.ask'))

    def put(self, uid):
        form = TopicForm()
        if form.validate_on_submit():
            pass

    def delete(self, uid):
        return 'delete'


class ReplyAPI(MethodView):
    decorators = [reply_permission]

    def post(self, uid):
        form = ReplyForm()
        topic = Topic.query.filter_by(id=uid).first()
        if form.validate_on_submit():
            SQLData.set_replies(form, uid)
            return redirect('/topic/' + topic.uid)
        else:
            if form.errors:
                flash_errors(form)
            else:
                pass
            return redirect(url_for('topic.topic',
                                    uid=str(topic.uid),
                                    _anchor='comment'))

    def put(self, uid):
        return 'put'

    def delete(self, uid):
        return 'delete'

topic_view = TopicAPI.as_view('topic')
site.add_url_rule('/topic',
                  defaults={'uid': None},
                  view_func=topic_view,
                  methods=['GET', ])
site.add_url_rule('/topic', view_func=topic_view, methods=['POST', ])
site.add_url_rule('/topic/<uid>',
                  view_func=topic_view,
                  methods=['GET', 'PUT', 'DELETE'])

site.add_url_rule('/reply/<uid>',
                  view_func=ReplyAPI.as_view('reply'),
                  methods=['POST', 'PUT'])
