#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 18:04:43 (CST)
# Last Update:星期二 2016-6-14 23:20:13 (CST)
#          By:
# Description:
# **************************************************************************
from flask import (Blueprint, render_template, request, redirect, url_for,
                   jsonify)
from flask.views import MethodView
from flask_maple.forms import flash_errors
from flask_login import current_user
from flask_maple.forms import return_errors
from maple import app, db
from maple.main.permission import follow_permission, collect_permission
from maple.helpers import is_num
from maple.topic.models import Topic, Reply, Collect, Tags
from maple.forums.models import Notice
from maple.user.models import User
from maple.mine.forms import CollectForm

site = Blueprint('mine', __name__)


class CollectAPI(MethodView):
    decorators = [collect_permission]

    def template_with_uid(self, topics, collect):
        form = CollectForm()
        form.name.data = collect.name
        form.description.data = collect.description
        form.is_privacy.data = 0 if collect.is_privacy else 1
        data = {'topics': topics, 'collect': collect, 'form': form}
        return render_template('mine/collect.html', **data)

    def template_without_uid(self, collects):
        form = CollectForm()
        data = {'collects': collects, 'form': form}
        return render_template('mine/collect_list.html', **data)

    def get(self, uid):
        page = is_num(request.args.get('page'))
        if uid is None:
            topics = current_user.collects.paginate(page,
                                                    app.config['PER_PAGE'],
                                                    error_out=True)
            return self.template_without_uid(topics)
        else:
            collect = Collect.query.filter_by(id=uid).first()
            topics = collect.topics.paginate(page, 10, True)
            return self.template_with_uid(topics, collect)

    def post(self):
        form = CollectForm()
        if form.validate_on_submit():
            collect = Collect()
            collect.name = form.name.data
            collect.description = form.description.data
            collect.is_privacy = True if form.is_privacy.data == 0 else False
            collect.author = current_user
            current_user.following_collects.append(collect)
            db.session.add(collect)
            db.session.commit()
            return redirect(url_for('mine.collect'))
        else:
            if form.errors:
                flash_errors(form)
            return redirect(url_for('mine.collect'))

    def put(self, uid):
        form = CollectForm()
        if form.validate_on_submit():
            collect = Collect.query.filter_by(id=uid).first_or_404()
            collect.name = form.name.data
            collect.description = form.description.data
            collect.is_privacy = True if form.is_privacy.data == 0 else False
            db.session.commit()
            return jsonify(judge=True)
        else:
            if form.errors:
                return return_errors(form)
            return jsonify(judge=False)

    def delete(self, uid):
        collect = Collect.query.filter_by(id=uid).first_or_404()
        db.session.delete(collect)
        db.session.commit()
        return jsonify(judge=True)


@site.route('/collect/following')
def collect_following():
    return redirect(url_for('mine.follow', type='collect'))


@site.route('/add-to-collect', methods=['POST'])
def add_collect():
    form = request.form.getlist('add-to-collect')
    topicId = request.args.get('topicId')
    topic = Topic.query.filter_by(uid=topicId).first_or_404()
    for id in form:
        collect = Collect.query.filter_by(id=id).first_or_404()
        collect.topics.append(topic)
        db.session.commit()
    return redirect(url_for('topic.topic', uid=topic.uid))


class LikeAPI(MethodView):
    def get(self, uid):
        if uid is None:
            page = is_num(request.args.get('page'))
            replies = current_user.likes.paginate(page,
                                                  app.config['PER_PAGE'],
                                                  error_out=True)
            return render_template('mine/reply.html', replies=replies)
        else:
            return redirect(url_for('topic.reply', rid=uid))

    def post(self, uid):
        tid = request.args.get('tid')
        reply = Reply.query.filter_by(id=uid).first_or_404()
        current_user.likes.append(reply)
        db.session.commit()
        return redirect(url_for('topic.topic', uid=tid))

    def delete(self, uid):
        reply = Reply.query.filter_by(id=uid).first_or_404()
        db.session.delete(reply)
        db.session.commit()
        return 's'


class FollowAPI(MethodView):
    decorators = [follow_permission]

    def template_without_uid(self, topics):
        return render_template('mine/follow_list.html', follows=topics)

    def get(self, type):
        page = is_num(request.args.get('page'))
        if type == 'tag':
            return render_template('user/following_tag.html',
                                   following_type=type)
        elif type == 'user':
            return render_template('user/following_user.html',
                                   following_type=type)
        elif type == 'collect':
            return render_template('user/following_collect.html',
                                   following_type=type)
        else:
            return render_template('user/following_topic.html',
                                   following_type=type)

    def post(self):
        data = request.get_json()
        type = data['type']
        id = data['id']
        if type == 'tag':
            tag = Tags.query.filter_by(id=id).first()
            current_user.following_tags.append(tag)
            db.session.commit()
            return jsonify(judge=True)
        elif type == 'topic':
            topic = Topic.query.filter_by(id=id).first()
            current_user.following_topics.append(topic)
            db.session.commit()
            return jsonify(judge=True)
        elif type == 'user':
            user = User.query.filter_by(id=id).first()
            current_user.following_users.append(user)
            db.session.commit()
            return jsonify(judge=True)
        elif type == 'collect':
            collect = Collect.query.filter_by(id=id).first()
            current_user.following_collects.append(collect)
            db.session.commit()
            return jsonify(judge=True)
        else:
            pass
        return jsonify(judge=False)

    def delete(self):
        data = request.get_json()
        type = data['type']
        id = data['id']
        if type == 'tag':
            tag = Tags.query.filter_by(id=id).first()
            current_user.following_tags.remove(tag)
            db.session.commit()
            return jsonify(judge=True)
        elif type == 'topic':
            topic = Topic.query.filter_by(id=id).first()
            current_user.following_topics.remove(topic)
            db.session.commit()
            return jsonify(judge=True)
        elif type == 'user':
            pass
        elif type == 'collect':
            collect = Collect.query.filter_by(id=id).first()
            current_user.following_collects.remove(collect)
            db.session.commit()
            return jsonify(judge=True)
        else:
            pass
        return jsonify(judge=False)


class NoticeAPI(MethodView):
    def template_without_uid(self, notices):
        return render_template('topic/topic_good.html', notices=notices)

    def get(self, uid):
        if uid is None:
            page = is_num(request.args.get('page'))
            notices = Notice.query.filter_by(
                user=current_user.username).paginate(page,
                                                     app.config['PER_PAGE'],
                                                     error_out=True)
            return self.template_without_uid(notices)
        else:
            return redirect(url_for('topic.topic', uid=uid))

    def post(self, uid):
        topic = Topic.query.filter_by(uid=uid).first()
        topic.is_good = True
        db.session.commit()

    def put(self, uid):
        topic = Topic.query.filter_by(uid=uid).first()
        topic.is_good = False
        db.session.commit()


def register_api(view, endpoint, url):
    view_func = view.as_view(endpoint)
    site.add_url_rule(url,
                      defaults={'uid': None},
                      view_func=view_func,
                      methods=['GET', 'POST', 'DELETE'])


def register_draft(view, endpoint, url):
    view_func = view.as_view(endpoint)
    site.add_url_rule(url,
                      defaults={'uid': None},
                      view_func=view_func,
                      methods=['GET', 'POST'])
    site.add_url_rule('%s/<int:uid>' % url,
                      view_func=view_func,
                      methods=['GET', 'PUT', 'DELETE'])


collect_view = CollectAPI.as_view('collect')
site.add_url_rule('/collect',
                  defaults={'uid': None},
                  view_func=collect_view,
                  methods=['GET', ])
site.add_url_rule('/collect', view_func=collect_view, methods=['POST', ])
site.add_url_rule('/collect/<uid>',
                  view_func=collect_view,
                  methods=['GET', 'PUT', 'DELETE'])

follow_view = FollowAPI.as_view('follow')
site.add_url_rule('/follow',
                  defaults={'type': 'topics'},
                  view_func=follow_view,
                  methods=['GET', ])
site.add_url_rule('/follow', view_func=follow_view, methods=['POST', 'DELETE'])
site.add_url_rule('/follow/<type>', view_func=follow_view, methods=['GET'])
register_api(LikeAPI, 'like', '/likes')
# register_api(FollowAPI, 'follow', '/follows')
# register_api(DraftAPI, 'draft', '/draft')
# register_api(CollectAPI, 'collect', '/collects')
# register_api(LikeAPI, 'like', '/likes')
# register_api(FollowAPI, 'follow', '/follows')
# register_api(InviteAPI, 'invite', '/invites')
