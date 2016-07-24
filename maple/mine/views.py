#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 18:04:43 (CST)
# Last Update:星期日 2016-7-24 17:16:21 (CST)
#          By:
# Description:
# **************************************************************************
from flask import (render_template, request, redirect, url_for, jsonify,
                   current_app)
from flask.views import MethodView
from flask_maple.forms import flash_errors
from flask_login import current_user
from flask_maple.forms import return_errors
from maple import app
from maple.helpers import is_num
from maple.topic.models import Collect
from maple.mine.forms import CollectForm
from .controls import CollectModel, FollowModel, LikeModel, CollectDetail
from .permission import (follow_permission, collect_permission,
                         collect_detail_permission, like_permission)


class CollectAPI(MethodView):
    decorators = [collect_permission]

    def template_without_uid(self, data):
        form = CollectForm()
        data_form = {'form': form}
        data.update(data_form)
        return render_template('mine/collect_list.html', **data)

    def get(self, collectId):
        if collectId is None:
            page = is_num(request.args.get('page'))
            collects = current_user.collects.paginate(page,
                                                      app.config['PER_PAGE'],
                                                      error_out=True)
            data = {'collects': collects}
            return self.template_without_uid(data)
        else:
            return redirect(url_for('mine.collect_detail',
                                    collectId=collectId))

    def post(self):
        form = CollectForm()
        if form.validate_on_submit():
            CollectModel.post_data(form)
            return redirect(url_for('mine.collect'))
        else:
            if form.errors:
                flash_errors(form)
            return redirect(url_for('mine.collect'))

    def put(self, collectId):
        form = CollectForm()
        if form.validate_on_submit():
            CollectModel.put_data(form, collectId)
            return jsonify(judge=True)
        else:
            if form.errors:
                return return_errors(form)
            return jsonify(judge=False)

    def delete(self, collectId):
        CollectModel.delete_data(collectId)
        return jsonify(judge=True)


def collect_following():
    return redirect(url_for('mine.follow', type='collect'))


class CollectDetailAPI(MethodView):
    decorators = [collect_detail_permission]

    def template_with_uid(self, data):
        form = CollectForm()
        collect = data['collect']
        form.name.data = collect.name
        form.description.data = collect.description
        form.is_privacy.data = 0 if collect.is_privacy else 1
        data_form = {'form': form}
        data.update(data_form)
        return render_template('mine/collect.html', **data)

    def get(self, collectId):
        if collectId is not None:
            page = is_num(request.args.get('page'))
            collect = Collect.query.filter_by(id=collectId).first_or_404()
            topics = collect.topics.paginate(page, 10, True)
            data = {'collect': collect, 'topics': topics}
            return self.template_with_uid(data)
        else:
            return redirect(url_for('mine.collect'))

    def post(self):
        form = request.form.getlist('add-to-collect')
        topicId = request.args.get('topicId')
        topic = CollectDetail.post(form, topicId)
        return redirect(url_for('topic.topic', topicId=topic.uid))

    def delete(self, collectId):
        data = request.get_json()
        topicId = data['topicId']
        CollectDetail.delete(topicId, collectId)
        print('删除细节')
        return jsonify(judge=True)


class LikeAPI(MethodView):
    decorators = [like_permission]

    def post(self, replyId):
        LikeModel.post_data(replyId)
        return jsonify(judge=True)

    def delete(self, replyId):
        LikeModel.delete_data(replyId)
        return jsonify(judge=True)


class FollowAPI(MethodView):
    decorators = [follow_permission]

    def get(self, type):
        page = is_num(request.args.get('page'))
        per_page = current_app.config['PER_PAGE']
        if type == 'tag':
            following = current_user.following_tags.paginate(page, per_page,
                                                             False)
            return render_template('follow/following_tag.html',
                                   following_type=type,
                                   following=following)
        elif type == 'user':
            following = current_user.following_users.paginate(page, per_page,
                                                              False)
            return render_template('follow/following_user.html',
                                   following_type=type,
                                   following=following)
        elif type == 'collect':
            following = current_user.following_collects.paginate(
                page, per_page, False)
            return render_template('follow/following_collect.html',
                                   following_type=type,
                                   following=following)
        else:
            following = current_user.following_topics.paginate(page, per_page,
                                                               False)
            return render_template('follow/following_topic.html',
                                   following_type=type,
                                   following=following)

    def post(self, type):
        data = request.get_json()
        id = data['id']
        FollowModel.post_data(type, id)
        return jsonify(judge=True)

    def delete(self, type):
        data = request.get_json()
        id = data['id']
        FollowModel.delete_data(type, id)
        return jsonify(judge=True)
