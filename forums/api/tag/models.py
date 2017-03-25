#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: models.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-15 20:46:13 (CST)
# Last Update:星期六 2017-3-25 18:17:15 (CST)
#          By:
# Description:
# **************************************************************************
from flask_maple.models import ModelMixin
from forums.api.topic.models import Topic
from forums.api.user.models import User
from forums.extension import db

tags_follow_users = db.Table(
    'tags_follow_users',
    db.Column('tags_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('follow_users_id', db.Integer, db.ForeignKey('users.id')))

tags_topics = db.Table(
    'tags_topics', db.Column('tags_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('topics_id', db.Integer, db.ForeignKey('topics.id')))

tags_parents = db.Table(
    'tags_parents', db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('parent_id', db.Integer, db.ForeignKey('tags.id')))


class Tags(db.Model, ModelMixin):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(128), nullable=False)
    parents = db.relationship(
        'Tags',
        secondary=tags_parents,
        primaryjoin=(id == tags_parents.c.tag_id),
        secondaryjoin=(id == tags_parents.c.parent_id),
        backref=db.backref(
            'children', lazy='joined'),
        lazy='joined')
    topics = db.relationship(
        Topic,
        secondary=tags_topics,
        backref=db.backref(
            'tags', lazy='dynamic'),
        lazy='dynamic')
    followers = db.relationship(
        User,
        secondary=tags_follow_users,
        backref=db.backref(
            'following_tags', lazy='dynamic'),
        lazy='dynamic')

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Tags %r>' % self.name
