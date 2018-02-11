#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: models.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-15 20:52:07 (CST)
# Last Update: 星期日 2018-02-11 15:06:01 (CST)
#          By:
# Description:
# **************************************************************************
from datetime import datetime

from flask import current_app
from flask_login import current_user

from flask_maple.models import ModelMixin, ModelTimeMixin, ModelUserMixin
from forums.api.forums.models import Board
from forums.api.user.models import User
from forums.common.models import CommonUserMixin
from forums.extension import db
from forums.count import Count
from forums.jinja import safe_markdown, safe_clean, markdown

topic_follower = db.Table(
    'topic_follower',
    db.Column('topic_id', db.Integer, db.ForeignKey('topics.id')),
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')))


class Topic(db.Model, ModelMixin):
    __tablename__ = 'topics'
    __searchable__ = ['title', 'content']

    CONTENT_TYPE_TEXT = '0'
    CONTENT_TYPE_MARKDOWN = '1'
    CONTENT_TYPE_ORGMODE = '2'

    CONTENT_TYPE = (('0', 'text'), ('1', 'markdown'), ('2', 'org-mode'))

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(81), nullable=False)
    content = db.Column(db.Text, nullable=False)
    content_type = db.Column(
        db.String(10), nullable=False, default=CONTENT_TYPE_MARKDOWN)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow(), nullable=False)

    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
    is_good = db.Column(db.Boolean, default=False)
    is_top = db.Column(db.Boolean, default=False)
    author_id = db.Column(
        db.Integer, db.ForeignKey(
            'user.id', ondelete="CASCADE"))
    author = db.relationship(
        User,
        backref=db.backref(
            'topics', cascade='all,delete-orphan', lazy='dynamic'),
        lazy='joined')
    board_id = db.Column(
        db.Integer, db.ForeignKey(
            'boards.id', ondelete="CASCADE"))
    board = db.relationship(
        Board,
        backref=db.backref(
            'topics', cascade='all,delete-orphan', lazy='dynamic'),
        lazy='joined')
    followers = db.relationship(
        User,
        secondary=topic_follower,
        backref=db.backref(
            'following_topics', lazy='dynamic'),
        lazy='dynamic')

    __mapper_args__ = {"order_by": created_at.desc()}

    def is_followed(self, user=None):
        if user is None:
            user = current_user
        return db.session.query(topic_follower).filter(
            topic_follower.c.topic_id == self.id,
            topic_follower.c.follower_id == user.id).exists()

    def is_collected(self, user=None):
        if user is None:
            user = current_user
        return self.collects.filter_by(author_id=user.id).exists()

    @property
    def text(self):
        if self.content_type == Topic.CONTENT_TYPE_TEXT:
            return safe_clean(self.content)
        elif self.content_type == Topic.CONTENT_TYPE_MARKDOWN:
            return markdown(self.content)
        return self.content

    @property
    def newest_reply(self):
        return self.replies.order_by('-id').first()

    @property
    def reply_count(self):
        return Count.topic_reply_count(self.id)

    @reply_count.setter
    def reply_count(self, value):
        return Count.topic_reply_count(self.id, value)

    @property
    def read_count(self):
        return Count.topic_read_count(self.id)

    @read_count.setter
    def read_count(self, value):
        return Count.topic_read_count(self.id, value)

    def __str__(self):
        return self.title

    def __repr__(self):
        return "<Topic %r>" % self.title


reply_liker = db.Table(
    'reply_liker',
    db.Column('reply_id', db.Integer, db.ForeignKey('replies.id')),
    db.Column('liker_id', db.Integer, db.ForeignKey('user.id')))


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

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship(
        User, backref=db.backref(
            'replies', lazy='dynamic'), lazy='joined')

    likers = db.relationship(
        User,
        secondary=reply_liker,
        backref=db.backref(
            'like_replies', lazy='dynamic'),
        lazy='dynamic')

    def is_liked(self, user=None):
        if user is None:
            user = current_user
            if not user.is_authenticated:
                return False
        return self.likers.filter_by(id=user.id).exists()

    @property
    def liker_count(self):
        return Count.reply_liker_count(self.id)

    @liker_count.setter
    def liker_count(self, value):
        return Count.reply_liker_count(self.id, value)

    def __str__(self):
        return self.content[:10]

    def __repr__(self):
        return "<Topic %r>" % self.content[:10]
