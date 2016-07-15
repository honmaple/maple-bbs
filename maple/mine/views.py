#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 18:04:43 (CST)
# Last Update:星期五 2016-7-15 19:22:46 (CST)
#          By:
# Description:
# **************************************************************************
from flask import (Blueprint, render_template, request, redirect, url_for,
                   flash, jsonify)
from flask.views import MethodView
from flask_maple.forms import flash_errors
from flask_login import current_user, login_required
from flask_maple.forms import return_errors
from maple import app, db
from maple.main.permission import (follow_permission, collect_permission,
                                   like_permission)
from maple.helpers import is_num
from maple.topic.models import Topic, Collect
from maple.mine.forms import CollectForm
from .controls import CollectModel, FollowModel, LikeModel, CollectDetail

# site = Blueprint('mine', __name__)


class CollectAPI(MethodView):
    decorators = [collect_permission]

    def template_with_uid(self, data):
        form = CollectForm()
        collect = data['collect']
        form.name.data = collect.name
        form.description.data = collect.description
        form.is_privacy.data = 0 if collect.is_privacy else 1
        data_form = {'form': form}
        data.update(data_form)
        return render_template('mine/collect.html', **data)

    def template_without_uid(self, data):
        form = CollectForm()
        data_form = {'form': form}
        data.update(data_form)
        return render_template('mine/collect_list.html', **data)

    def get(self, uid):
        page = is_num(request.args.get('page'))
        if uid is None:
            collects = current_user.collects.paginate(page,
                                                      app.config['PER_PAGE'],
                                                      error_out=True)
            data = {'collects': collects}
            return self.template_without_uid(data)
        else:
            collect = Collect.query.filter_by(id=uid).first()
            topics = collect.topics.paginate(page, 10, True)
            data = {'collect': collect, 'topics': topics}
            return self.template_with_uid(data)

    def post(self):
        form = CollectForm()
        if form.validate_on_submit():
            CollectModel.post_data(form)
            return redirect(url_for('mine.collect'))
        else:
            if form.errors:
                flash_errors(form)
            return redirect(url_for('mine.collect'))

    def put(self, uid):
        form = CollectForm()
        if form.validate_on_submit():
            CollectModel.put_data(form, uid)
            return jsonify(judge=True)
        else:
            if form.errors:
                return return_errors(form)
            return jsonify(judge=False)

    def delete(self, uid):
        CollectModel.delete_data(uid)
        return jsonify(judge=True)


# @site.route('/collect/following')
def collect_following():
    return redirect(url_for('mine.follow', type='collect'))


# @site.route('/add-to-collect', methods=['POST'])
@login_required
def add_collect():
    form = request.form.getlist('add-to-collect')
    topicId = request.args.get('topicId')
    topic = CollectDetail.post(form, topicId)
    return redirect(url_for('topic.topic', uid=topic.uid))


# @site.route('/delete-from-collect', methods=['DELETE'])
@login_required
def delete_collect():
    data = request.get_json()
    topicId = data['topicId']
    collectId = data['collectId']
    CollectDetail.delete(topicId, collectId)
    return jsonify(judge=True)


class LikeAPI(MethodView):
    decorators = [like_permission]

    def post(self):
        data = request.get_json()
        uid = data['uid']
        LikeModel.post_data(uid)
        return jsonify(judge=True)

    def delete(self):
        data = request.get_json()
        uid = data['uid']
        LikeModel.delete_data(uid)
        return jsonify(judge=True)


class FollowAPI(MethodView):
    decorators = [follow_permission]

    def get(self, type):
        # page = is_num(request.args.get('page'))
        if type == 'tag':
            return render_template('follow/following_tag.html',
                                   following_type=type)
        elif type == 'user':
            return render_template('follow/following_user.html',
                                   following_type=type)
        elif type == 'collect':
            return render_template('follow/following_collect.html',
                                   following_type=type)
        else:
            return render_template('follow/following_topic.html',
                                   following_type=type)

    def post(self):
        data = request.get_json()
        type = data['type']
        id = data['id']
        type_list = ['tag', 'topic', 'user', 'collect']
        if type in type_list:
            FollowModel.post_data(type, id)
            return jsonify(judge=True)
        else:
            pass
        return jsonify(judge=False)

    def delete(self):
        data = request.get_json()
        type = data['type']
        id = data['id']
        type_list = ['tag', 'topic', 'user', 'collect']
        if type in type_list:
            FollowModel.delete_data(type, id)
            return jsonify(judge=True)
        else:
            pass
        return jsonify(judge=False)
