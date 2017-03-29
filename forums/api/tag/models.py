#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: models.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-15 20:46:13 (CST)
# Last Update:星期三 2017-3-29 19:17:5 (CST)
#          By:
# Description:
# **************************************************************************
from flask_login import current_user
from flask_maple.models import ModelMixin
from forums.api.topic.models import Topic
from forums.api.user.models import User
from forums.extension import db

tag_follower = db.Table(
    'tag_follower', db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')))

tag_topic = db.Table(
    'tag_topic', db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('topic_id', db.Integer, db.ForeignKey('topics.id')))


class Tags(db.Model, ModelMixin):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(128), nullable=False)
    parent_id = db.Column(
        db.Integer, db.ForeignKey(
            'tags.id', ondelete="CASCADE"))
    parent = db.relationship(
        'Tags',
        remote_side=[id],
        backref=db.backref(
            'children',
            remote_side=[parent_id],
            cascade='all,delete-orphan',
            lazy='dynamic'),
        lazy='joined',
        uselist=False)
    topics = db.relationship(
        Topic,
        secondary=tag_topic,
        backref=db.backref(
            'tags', lazy='dynamic'),
        lazy='dynamic')
    followers = db.relationship(
        User,
        secondary=tag_follower,
        backref=db.backref(
            'following_tags', lazy='dynamic'),
        lazy='dynamic')

    def is_followed(self, user=None):
        if user is None:
            user = current_user
        return db.session.query(tag_follower).filter(
            tag_follower.c.tag_id == self.id,
            tag_follower.c.follower_id == user.id).exists()

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Tags %r>' % self.name
