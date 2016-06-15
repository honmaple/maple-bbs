#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 13:47:04 (CST)
# Last Update:星期三 2016-6-15 19:3:17 (CST)
#          By:
# Description:
# **************************************************************************
from flask import (Blueprint, render_template, redirect, url_for, request)
from flask.views import MethodView
from flask_login import login_required
from flask_maple.forms import flash_errors
from maple import app
from maple.main.models import RedisData
from maple.main.permission import topic_permission, reply_permission
from maple.helpers import is_num
from maple.forums.models import Board
from maple.topic.models import Topic
from maple.topic.forms import TopicForm, ReplyForm
from .controls import TopicModel, ReplyModel

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


@site.route('/good')
def good():
    page = is_num(request.args.get('page'))
    topics = Topic.query.filter_by(is_good=True).paginate(
        page, app.config['PER_PAGE'],
        error_out=True)
    return render_template('topic/topic_good.html', topics=topics)


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
            topic = TopicModel.post_data(form)
            return redirect(url_for('topic.topic', uid=topic.uid))
        else:
            if form.errors:
                flash_errors(form)
                form.title.data = form.title.data
            else:
                pass
            form.title.data = form.title.data
            return redirect(url_for('topic.ask'))

    # def put(self, uid):
    #     form = TopicForm()
    #     if form.validate_on_submit():
    #         pass

    # def delete(self, uid):
    #     return 'delete'


class ReplyAPI(MethodView):
    decorators = [reply_permission]

    def post(self, uid):
        form = ReplyForm()
        topic = Topic.query.filter_by(id=uid).first()
        if form.validate_on_submit():
            ReplyModel.post_data(form, uid)
            return redirect(url_for('topic.topic', uid=topic.uid))
        else:
            if form.errors:
                flash_errors(form)
            else:
                pass
            return redirect(url_for('topic.topic',
                                    uid=str(topic.uid),
                                    _anchor='reply'))

    # def put(self, uid):
    #     return 'put'

    # def delete(self, uid):
    #     return 'delete'


topic_view = TopicAPI.as_view('topic')
site.add_url_rule('',
                  defaults={'uid': None},
                  view_func=topic_view,
                  methods=['GET'])
site.add_url_rule('', view_func=TopicAPI.as_view('post'), methods=['POST'])
site.add_url_rule('/<uid>', view_func=topic_view, methods=['GET'])

site.add_url_rule('/reply/<uid>',
                  view_func=ReplyAPI.as_view('reply'),
                  methods=['POST'])
