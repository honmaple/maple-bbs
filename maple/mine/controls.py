#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: controls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-06-15 09:44:01 (CST)
# Last Update:星期日 2016-7-24 13:58:50 (CST)
#          By:
# Description:
# **************************************************************************
from flask import flash
from flask_login import current_user
from maple import db
from maple.topic.models import Collect, Topic, Reply
from maple.tag.models import Tags
from maple.user.models import User
from maple.forums.controls import collect as notice_collect
from maple.forums.controls import like as notice_like
from maple.forums.controls import user as notice_user


class CollectDetail(object):
    def post(form, topicId):
        topic = Topic.query.filter_by(uid=topicId).first_or_404()
        for id in form:
            '''This has a problem'''
            collect = Collect.query.filter_by(id=id).first_or_404()
            if topic in collect.topics:
                flash('This topic has been collected in %s' % collect.name,
                      'warning')
            else:
                collect.topics.append(topic)
                db.session.commit()
                if topic.author_id != current_user.id:
                    notice_collect(topic)
        return topic

    def delete(topicId, collectId):
        topic = Topic.query.filter_by(uid=topicId).first_or_404()
        collect = Collect.query.filter_by(id=collectId).first_or_404()
        collect.topics.remove(topic)
        db.session.commit()


class CollectModel(object):
    def post_data(form):
        collect = Collect()
        collect.name = form.name.data
        collect.description = form.description.data
        collect.is_privacy = True if form.is_privacy.data == 0 else False
        collect.author = current_user
        current_user.following_collects.append(collect)
        db.session.add(collect)
        db.session.commit()

    def put_data(form, uid):
        collect = Collect.query.filter_by(id=uid).first_or_404()
        collect.name = form.name.data
        collect.description = form.description.data
        collect.is_privacy = True if form.is_privacy.data == 0 else False
        db.session.commit()

    def delete_data(uid):
        collect = Collect.query.filter_by(id=uid).first_or_404()
        db.session.delete(collect)
        db.session.commit()


class FollowModel(object):
    def post_data(type, id):
        if type == 'tag':
            tag = Tags.query.filter_by(id=id).first_or_404()
            current_user.following_tags.append(tag)
            db.session.commit()
        elif type == 'topic':
            topic = Topic.query.filter_by(id=id).first_or_404()
            current_user.following_topics.append(topic)
            db.session.commit()
        elif type == 'user':
            user = User.query.filter_by(id=id).first_or_404()
            current_user.following_users.append(user)
            db.session.commit()
            notice_user(user.id)
        elif type == 'collect':
            collect = Collect.query.filter_by(id=id).first_or_404()
            current_user.following_collects.append(collect)
            db.session.commit()

    def delete_data(type, id):
        if type == 'tag':
            tag = Tags.query.filter_by(id=id).first_or_404()
            current_user.following_tags.remove(tag)
            db.session.commit()
        elif type == 'topic':
            topic = Topic.query.filter_by(id=id).first_or_404()
            current_user.following_topics.remove(topic)
            db.session.commit()
        elif type == 'user':
            user = User.query.filter_by(id=id).first_or_404()
            current_user.following_users.remove(user)
            db.session.commit()
        elif type == 'collect':
            collect = Collect.query.filter_by(id=id).first_or_404()
            current_user.following_collects.remove(collect)
            db.session.commit()


class LikeModel(object):
    def post_data(uid):
        reply = Reply.query.filter_by(id=uid).first_or_404()
        current_user.likes.append(reply)
        db.session.commit()
        if reply.author_id != current_user.id:
            notice_like(reply)

    def delete_data(uid):
        reply = Reply.query.filter_by(id=uid).first_or_404()
        current_user.likes.remove(reply)
        db.session.commit()
