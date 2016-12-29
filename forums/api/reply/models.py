#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: models.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-15 20:50:44 (CST)
# Last Update:星期四 2016-12-15 23:20:31 (CST)
#          By:
# Description:
# **************************************************************************
from flask_maple.models import ModelMixin
from maple.extension import db
from datetime import datetime
from api.topic.models import Topic
from api.user.models import User

replies_likers = db.Table(
    'replies_likers',
    db.Column('replies_id', db.Integer, db.ForeignKey('replies.id')),
    db.Column('likers_id', db.Integer, db.ForeignKey('users.id')))


class Reply(db.Model, ModelMixin):
    __tablename__ = 'replies'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
    topic_id = db.Column(
        db.Integer, db.ForeignKey(
            'topics.id', ondelete="CASCADE"))
    topic = db.relationship(
        Topic,
        backref=db.backref(
            'replies', cascade='all,delete-orphan', lazy='dynamic'),
        lazy='joined')

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship(
        User, backref=db.backref(
            'replies', lazy='dynamic'), lazy='joined')

    likers = db.relationship(
        User,
        secondary=replies_likers,
        backref=db.backref(
            'like_replies', lazy='dynamic'),
        lazy='dynamic')

    def __str__(self):
        return self.content[:10]

    def __repr__(self):
        return "<Topic %r>" % self.content[:10]
