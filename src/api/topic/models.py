#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: models.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-15 20:52:07 (CST)
# Last Update:星期三 2017-1-25 20:25:8 (CST)
#          By:
# Description:
# **************************************************************************
from flask import current_app
from flask_maple.models import ModelMixin
from forums.extension import db
from datetime import datetime
from api.user.models import User
from api.board.models import Board

topics_follow_users = db.Table(
    'topics_follow_users',
    db.Column('topics_id', db.Integer, db.ForeignKey('topics.id')),
    db.Column('follow_users_id', db.Integer, db.ForeignKey('users.id')))


class Topic(db.Model, ModelMixin):
    __tablename__ = 'topics'

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
            'users.id', ondelete="CASCADE"))
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
        secondary=topics_follow_users,
        backref=db.backref(
            'following_topics', lazy='dynamic'),
        lazy='dynamic')

    def __str__(self):
        return self.title

    def __repr__(self):
        return "<Topic %r>" % self.title


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
    privacy = db.Column(db.Boolean, default=False)
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
        Topic,
        secondary=topics_collects,
        backref=db.backref(
            'collects', lazy='dynamic'),
        lazy='dynamic')

    followers = db.relationship(
        User,
        secondary=collect_follow_users,
        backref=db.backref(
            'following_collects', lazy='dynamic'),
        lazy='dynamic')

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Collect %r>" % self.name
