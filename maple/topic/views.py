#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 13:47:04 (CST)
# Last Update:星期一 2016-6-27 14:30:59 (CST)
#          By:
# Description:
# **************************************************************************
from flask import (Blueprint, render_template, redirect, url_for, request, g,
                   jsonify, session, Markup, abort)
from flask.views import MethodView
from flask_login import login_required
from flask_maple.forms import flash_errors
from maple import app, db
from maple.main.models import RedisData
from maple.main.permission import topic_permission, reply_permission
from maple.helpers import is_num
from maple.forums.models import Board
from maple.topic.models import Topic
from maple.topic.forms import TopicForm, ReplyForm
from maple.filters import safe_clean, Filters
from .controls import TopicModel, ReplyModel

site = Blueprint('topic', __name__)


@site.route('/ask')
@login_required
def ask():
    form = session.get('topicform', None)
    if form is None:
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


@site.route('/preview', methods=['GET', 'POST'])
@login_required
def preview():
    if request.method == "POST":
        choice = request.values.get('choice')
        content = request.values.get('content')
        print(choice)
        if choice == '2':
            return safe_clean(content)
        else:
            return Filters.safe_markdown(content)
    else:
        abort(404)


@site.route('/up/<topicId>', methods=['POST'])
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


@site.route('/down/<topicId>', methods=['POST'])
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
                page, app.config['PER_PAGE'],
                error_out=True)
            top_topics = Topic.query.filter_by(is_top=True).limit(5).all()
            data = {'topics': topics, 'top_topics': top_topics}
            return self.template_without_uid(data)
        else:
            form = ReplyForm()
            topic = Topic.query.filter_by(uid=str(uid)).first_or_404()
            replies = topic.replies.paginate(page, app.config['PER_PAGE'],
                                             True)
            RedisData.set_read_count(topic.id)
            data = {'form': form, 'topic': topic, 'replies': replies}
            return self.template_with_uid(data)

    def post(self):
        form = TopicForm()
        if form.validate_on_submit():
            topic = TopicModel.post_data(form)
            return redirect(url_for('topic.topic', uid=topic.uid))
        else:
            if form.errors:
                flash_errors(form)
            session['topicform'] = form
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
            return redirect(url_for('topic.topic',
                                    uid=topic.uid,
                                    _anchor='replies-content'))
        else:
            if form.errors:
                flash_errors(form)
            else:
                pass
            return redirect(url_for('topic.topic',
                                    uid=str(topic.uid),
                                    _anchor='replies-content'))

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
