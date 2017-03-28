#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: models.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-03-28 17:58:59 (CST)
# Last Update:星期二 2017-3-28 18:4:27 (CST)
#          By:
# Description:
# **************************************************************************
from datetime import datetime
from flask_maple.models import ModelMixin, ModelTimeMixin, ModelUserMixin
from forums.api.user.models import User
from forums.extension import db

topics_collects = db.Table(
    'topics_collects',
    db.Column('topics_id', db.Integer, db.ForeignKey('topics.id')),
    db.Column('collects_id', db.Integer, db.ForeignKey('collects.id')))

collect_follow_users = db.Table(
    'collects_follow_users',
    db.Column('collects_id', db.Integer, db.ForeignKey('collects.id')),
    db.Column('follow_users_id', db.Integer, db.ForeignKey('users.id')))


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
            'users.id', ondelete="CASCADE"))
    author = db.relationship(
        User,
        backref=db.backref(
            'collects', cascade='all,delete-orphan', lazy='dynamic'),
        lazy='joined')

    topics = db.relationship(
        'Topic',
        secondary=topics_collects,
        backref=db.backref(
            'collects', lazy='dynamic'),
        lazy='dynamic')

    followers = db.relationship(
        'User',
        secondary=collect_follow_users,
        backref=db.backref(
            'following_collects', lazy='dynamic'),
        lazy='dynamic')

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Collect %r>" % self.name
