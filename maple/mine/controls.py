#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: controls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-06-15 09:44:01 (CST)
# Last Update:星期三 2016-6-15 13:11:34 (CST)
#          By:
# Description:
# **************************************************************************
from flask_login import current_user
from maple import db
from maple.topic.models import Collect, Topic, Tags, Reply
from maple.user.models import User


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
            tag = Tags.query.filter_by(id=id).first()
            current_user.following_tags.append(tag)
            db.session.commit()
        elif type == 'topic':
            topic = Topic.query.filter_by(id=id).first()
            current_user.following_topics.append(topic)
            db.session.commit()
        elif type == 'user':
            user = User.query.filter_by(id=id).first()
            current_user.following_users.append(user)
            db.session.commit()
        elif type == 'collect':
            collect = Collect.query.filter_by(id=id).first()
            current_user.following_collects.append(collect)
            db.session.commit()

    def delete_data(type, id):
        if type == 'tag':
            tag = Tags.query.filter_by(id=id).first()
            current_user.following_tags.remove(tag)
            db.session.commit()
        elif type == 'topic':
            topic = Topic.query.filter_by(id=id).first()
            current_user.following_topics.remove(topic)
            db.session.commit()
        elif type == 'user':
            pass
        elif type == 'collect':
            collect = Collect.query.filter_by(id=id).first()
            current_user.following_collects.remove(collect)
            db.session.commit()


class LikeModel(object):
    def post_data(uid):
        reply = Reply.query.filter_by(id=uid).first_or_404()
        current_user.likes.append(reply)
        db.session.commit()

    def delete_data(uid):
        reply = Reply.query.filter_by(id=uid).first_or_404()
        current_user.likes.remove(reply)
        db.session.commit()
