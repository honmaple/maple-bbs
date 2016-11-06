#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 13:47:04 (CST)
# Last Update:星期日 2016-11-6 11:3:17 (CST)
#          By:
# Description:
# **************************************************************************
from flask import (render_template, redirect, url_for, request, jsonify,
                   current_app)
from flask.views import MethodView
from flask_login import login_required
from flask_maple.forms import flash_errors, return_errors
from flask_babelex import gettext as _
from maple import db
from maple.helpers import replies_page
from maple.helpers import is_num
from maple.forums.models import Board
from maple.filters import safe_clean, Filters
from .models import Topic
from .forms import TopicForm, ReplyForm
from .controls import TopicModel, ReplyModel, vote
from .permission import (topic_permission, reply_permission, ask_permission,
                         vote_permission, preview_permission, edit_permission)


class TopicBaseView(MethodView):
    form = TopicForm

    def get_sort_tuple(self):
        sort_tuple = ()
        return sort_tuple

    def get_filter_dict(self):
        filter_dict = {}
        return filter_dict

    def get_page_info(self):
        page = request.args.get('page', 1, type=int)
        number = request.args.get('number', 20, type=int)
        return page, number


class TopicAskView(TopicBaseView):
    decorators = [ask_permission, login_required]

    def get(self):
        boardId = request.args.get('boardId', type=int)
        form = self.form()
        if boardId is not None:
            board = Board.query.filter_by(id=boardId).first()
            form.category.data = board.id
        data = {'title': _('Ask - '), 'form': form}
        return render_template('topic/ask.html', **data)


class TopicEditView(TopicBaseView):
    decorators = [edit_permission, login_required]

    def get(self, topicId):
        topic = Topic.query.filter_by(uid=topicId).first_or_404()
        form = self.form()
        form.title.data = topic.title
        form.category.data = topic.board_id
        form.tags.data = ','.join([tag.tagname for tag in topic.tags])
        form.content.data = topic.content
        data = {'title': _('Edit -'), 'form': form, 'topic': topic}
        return render_template('topic/edit.html', **data)


class TopicPreviewView(MethodView):
    decorators = [preview_permission, login_required]

    def post(self):
        choice = request.values.get('choice')
        content = request.values.get('content')
        if choice == '2':
            return safe_clean(content)
        else:
            return Filters.safe_markdown(content)


class TopicVoteView(MethodView):
    decorators = [vote_permission]

    def post(self, topicId):
        topic = Topic.query.filter_by(uid=topicId).first_or_404()
        if topic.vote == 0:
            topic.vote = 1
        else:
            topic.vote += 1
        db.session.commit()
        html = vote(topic.vote)
        return jsonify(judge=True, html=html)

    def delete(self, topicId):
        topic = Topic.query.filter_by(uid=topicId).first_or_404()
        if topic.vote == 0:
            topic.vote = -1
        else:
            topic.vote -= 1
        db.session.commit()
        html = vote(topic.vote)
        return jsonify(judge=True, html=html)


class TopicGoodListView(TopicBaseView):
    def get(self):
        page = is_num(request.args.get('page'))
        topics = Topic.query.filter_by(is_good=True).paginate(
            page, current_app.config['PER_PAGE'], error_out=True)
        data = {'title': _('Good Topics - '), 'topics': topics}
        return render_template('topic/topic_good.html', **data)


class TopicTopListView(TopicBaseView):
    def get(self):
        page = is_num(request.args.get('page'))
        topics = Topic.query.filter_by(is_top=True).paginate(
            page, current_app.config['PER_PAGE'], error_out=True)
        data = {'title': _('Top Topics - '), 'topics': topics}
        return render_template('topic/topic_top.html', **data)


class TopicListView(TopicBaseView):
    def get(self):
        page = is_num(request.args.get('page'))
        topics, top_topics = TopicModel.get_list(page)
        data = {
            'title': 'All Topics - ',
            'topics': topics,
            'top_topics': top_topics
        }
        return render_template('topic/topic.html', **data)

    def post(self):
        form = TopicForm()
        if form.validate_on_submit():
            topic = TopicModel.post(form)
            return redirect(url_for('topic.topic', topicId=topic.uid))
        else:
            if self.form.errors:
                flash_errors(form)
            return redirect(url_for('topic.ask'))


class TopicView(TopicBaseView):
    decorators = [topic_permission]

    def get(self, topicId):
        page = is_num(request.args.get('page'))
        order = request.args.get('orderby')
        form = ReplyForm()
        topic, replies = TopicModel.get_detail(page, topicId, order)
        data = {
            'title': '%s - ' % topic.title,
            'form': form,
            'topic': topic,
            'replies': replies
        }
        return render_template('topic/content.html', **data)

    def put(self, topicId):
        form = self.form()
        if form.validate_on_submit():
            TopicModel.put(form, topicId)
            return jsonify(judge=True)
        else:
            if form.errors:
                return_errors(form)
            return redirect(url_for('topic.ask'))

    def delete(self, topicId):
        return 'delete'


class ReplyListView(MethodView):
    decorators = [reply_permission, login_required]

    def post(self, topicId):
        form = ReplyForm()
        topic = Topic.query.filter_by(id=topicId).first_or_404()
        if form.validate_on_submit():
            rep = ReplyModel()
            reply = rep.post(form, topicId)
            page = replies_page(topic.id)
            return redirect(
                url_for(
                    'topic.topic',
                    topicId=topic.uid,
                    page=page,
                    _anchor='reply' + str(reply.id)))
        else:
            if form.errors:
                flash_errors(form)
            page = replies_page(topic.id)
            return redirect(
                url_for(
                    'topic.topic',
                    topicId=topic.uid,
                    page=page,
                    _anchor='content'))
