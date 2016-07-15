#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 13:47:04 (CST)
# Last Update:星期五 2016-7-15 20:24:16 (CST)
#          By:
# Description:
# **************************************************************************
from flask import (render_template, redirect, url_for, request, g, jsonify)
from flask.views import MethodView
from flask_login import login_required
from flask_maple.forms import flash_errors
from maple import app, db
from maple.helpers import replies_page
from maple.main.models import RedisData
from maple.main.permission import topic_permission, reply_permission
from maple.helpers import is_num
from maple.forums.models import Board
from maple.topic.models import Topic, Reply
from maple.topic.forms import TopicForm, ReplyForm
from maple.filters import safe_clean, Filters
from .controls import TopicModel, ReplyModel


@login_required
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
        page,
        app.config['PER_PAGE'],
        error_out=True)
    data = {'title': '精华文章 - ', 'topics': topics}
    return render_template('topic/topic_good.html', **data)


@login_required
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
    html = TopicModel.vote(topic.vote)
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
    html = TopicModel.vote(topic.vote)
    return jsonify(judge=True, html=html)


class TopicAPI(MethodView):
    decorators = [topic_permission]

    def template_with_uid(self, data):
        return render_template('topic/content.html', **data)

    def template_without_uid(self, data):
        return render_template('topic/topic.html', **data)

    def get(self, uid):
        page = is_num(request.args.get('page'))
        if uid is None:
            topics = Topic.query.filter_by(is_top=False).paginate(
                page,
                app.config['PER_PAGE'],
                error_out=True)
            top_topics = Topic.query.filter_by(is_top=True).limit(5).all()
            data = {'title': '所有主题 - ',
                    'topics': topics,
                    'top_topics': top_topics}
            return self.template_without_uid(data)
        else:
            form = ReplyForm()
            topic = Topic.query.filter_by(uid=str(uid)).first_or_404()
            replies = Reply.query.filter_by(
                topic_id=topic.id).order_by(Reply.publish.asc()).paginate(
                    page, app.config['PER_PAGE'], True)
            RedisData.set_read_count(topic.id)
            data = {'title': '%s - ' % topic.title,
                    'form': form,
                    'topic': topic,
                    'replies': replies}
            return self.template_with_uid(data)

    def post(self):
        form = TopicForm()
        if form.validate_on_submit():
            topic = TopicModel.post_data(form)
            return redirect(url_for('topic.topic', uid=topic.uid))
        else:
            if form.errors:
                flash_errors(form)
            return redirect(url_for('topic.ask'))

    def put(self, uid):
        return 'delete'

    def delete(self, uid):
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
                                    uid=topic.uid,
                                    page=page,
                                    _anchor='reply' + str(reply.id)))
        else:
            if form.errors:
                flash_errors(form)
            page = replies_page(topic.id)
            return redirect(url_for('topic.topic',
                                    uid=topic.uid,
                                    page=page,
                                    _anchor='replies-content'))

    # def put(self, uid):
    #     return 'put'

    # def delete(self, uid):
    #     return 'delete'
