#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 13:47:04 (CST)
# Last Update:星期四 2016-7-28 21:14:7 (CST)
#          By:
# Description:
# **************************************************************************
from flask import (render_template, redirect, url_for, request, g, jsonify,
                   current_app)
from flask.views import MethodView
from flask_login import login_required
from flask_maple.forms import flash_errors
from maple import db
from maple.helpers import replies_page
from maple.helpers import is_num
from maple.forums.models import Board
from maple.filters import safe_clean, Filters
from .models import Topic
from .forms import TopicForm, ReplyForm
from .controls import TopicModel, ReplyModel, vote
from .permission import (topic_permission, reply_permission, ask_permission,
                         preview_permission)


@login_required
@ask_permission
def ask():
    form = TopicForm()
    boardId = request.args.get('boardId')
    if boardId is not None:
        board = Board.query.filter_by(id=boardId).first()
        form.category.data = board.id

    data = {'title': '提问 - ', 'form': form}
    return render_template('topic/ask.html', **data)


def good():
    page = is_num(request.args.get('page'))
    topics = Topic.query.filter_by(is_good=True).paginate(
        page, current_app.config['PER_PAGE'],
        error_out=True)
    data = {'title': '精华文章 - ', 'topics': topics}
    return render_template('topic/topic_good.html', **data)


@login_required
@preview_permission
def preview():
    choice = request.values.get('choice')
    content = request.values.get('content')
    print(choice)
    if choice == '2':
        return safe_clean(content)
    else:
        return Filters.safe_markdown(content)


def vote_up(topicId):
    if not g.user.is_authenticated:
        return jsonify(judge=False, url=url_for('auth.login'))
    topic = Topic.query.filter_by(uid=topicId).first_or_404()
    if not topic.vote:
        topic.vote = 1
    else:
        topic.vote += 1
    db.session.commit()
    html = vote(topic.vote)
    return jsonify(judge=True, html=html)


def vote_down(topicId):
    if not g.user.is_authenticated:
        return jsonify(judge=False, url=url_for('auth.login'))
    topic = Topic.query.filter_by(uid=topicId).first_or_404()
    if not topic.vote:
        topic.vote = -1
    else:
        topic.vote -= 1
    db.session.commit()
    html = vote(topic.vote)
    return jsonify(judge=True, html=html)


class TopicAPI(MethodView):
    decorators = [topic_permission]

    def template_with_uid(self, data):
        return render_template('topic/content.html', **data)

    def template_without_uid(self, data):
        return render_template('topic/topic.html', **data)

    def get(self, topicId):
        page = is_num(request.args.get('page'))
        order = request.args.get('orderby')
        if topicId is None:
            topics, top_topics = TopicModel.get_list(page)
            data = {'title': '所有主题 - ',
                    'topics': topics,
                    'top_topics': top_topics}
            return self.template_without_uid(data)
        else:
            form = ReplyForm()
            topic, replies = TopicModel.get_detail(page, topicId, order)
            data = {'title': '%s - ' % topic.title,
                    'form': form,
                    'topic': topic,
                    'replies': replies}
            return self.template_with_uid(data)

    def post(self):
        form = TopicForm()
        if form.validate_on_submit():
            topic = TopicModel.post(form)
            return redirect(url_for('topic.topic', topicId=topic.uid))
        else:
            if form.errors:
                flash_errors(form)
            return redirect(url_for('topic.ask'))

    def put(self, topicId):
        return 'put'

    def delete(self, topicId):
        return 'delete'


class ReplyAPI(MethodView):
    decorators = [reply_permission]

    def post(self, topicId):
        form = ReplyForm()
        topic = Topic.query.filter_by(id=topicId).first_or_404()
        if form.validate_on_submit():
            reply = ReplyModel.post_data(form, topicId)
            page = replies_page(topic.id)
            return redirect(url_for('topic.topic',
                                    topicId=topic.uid,
                                    page=page,
                                    _anchor='reply' + str(reply.id)))
        else:
            if form.errors:
                flash_errors(form)
            page = replies_page(topic.id)
            return redirect(url_for('topic.topic',
                                    topicId=topic.uid,
                                    page=page,
                                    _anchor='replies-content'))

    # def put(self, uid):
    #     return 'put'

    # def delete(self, uid):
    #     return 'delete'
