#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: models.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-03-28 17:58:59 (CST)
# Last Update:星期三 2017-12-13 16:06:36 (CST)
#          By:
# Description:
# **************************************************************************
from datetime import datetime
from flask_maple.models import ModelMixin, ModelTimeMixin, ModelUserMixin
from flask_login import current_user
from forums.api.user.models import User
from forums.extension import db

topic_collect = db.Table(
    'topic_collect',
    db.Column('topic_id', db.Integer, db.ForeignKey('topics.id')),
    db.Column('collect_id', db.Integer, db.ForeignKey('collects.id')))

collect_follower = db.Table(
    'collect_follower',
    db.Column('collect_id', db.Integer, db.ForeignKey('collects.id')),
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')))


class Collect(db.Model, ModelMixin):
    __tablename__ = 'collects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(256), nullable=True)
    is_hidden = db.Column(db.Boolean, default=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
    author_id = db.Column(
        db.Integer, db.ForeignKey(
            'user.id', ondelete="CASCADE"))
    author = db.relationship(
        User,
        backref=db.backref(
            'collects', cascade='all,delete-orphan', lazy='dynamic'),
        lazy='joined')

    topics = db.relationship(
        'Topic',
        secondary=topic_collect,
        backref=db.backref(
            'collects', lazy='dynamic'),
        lazy='dynamic')

    followers = db.relationship(
        'User',
        secondary=collect_follower,
        backref=db.backref(
            'following_collects', lazy='dynamic'),
        lazy='dynamic')

    def is_followed(self, user=None):
        if user is None:
            user = current_user
        return db.session.query(collect_follower).filter(
            collect_follower.c.collect_id == self.id,
            collect_follower.c.follower_id == user.id).exists()

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Collect %r>" % self.name
