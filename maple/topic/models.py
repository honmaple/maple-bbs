#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: models.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 13:32:12 (CST)
# Last Update:星期六 2016-7-30 22:44:6 (CST)
#          By:
# Description:
# **************************************************************************
from flask import current_app
from maple import db
from datetime import datetime
from sqlalchemy import event


class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(36), nullable=False)
    title = db.Column(db.String(81), nullable=False)
    content = db.Column(db.Text, nullable=False)
    publish = db.Column(db.DateTime, default=datetime.utcnow())
    updated = db.Column(db.DateTime)
    vote = db.Column(db.Integer, default=0)

    author_id = db.Column(db.Integer,
                          db.ForeignKey('users.id',
                                        ondelete="CASCADE"))
    author = db.relationship('User',
                             backref=db.backref('topics',
                                                cascade='all,delete-orphan',
                                                lazy='dynamic'))
    board_id = db.Column(db.Integer,
                         db.ForeignKey('boards.id',
                                       ondelete="CASCADE"))
    board = db.relationship(
        'Board',
        backref=db.backref('topics',
                           cascade='all,delete-orphan',
                           lazy='dynamic',
                           order_by='Topic.publish.desc()'))

    is_good = db.Column(db.Boolean, default=False)
    is_top = db.Column(db.Boolean, default=False)
    # is_top = db.Column(db.Integer, default = 0)
    is_markdown = db.Column(db.Boolean, default=False)
    is_draft = db.Column(db.Boolean, default=False)

    __mapper_args__ = {"order_by": publish.desc()}

    def __str__(self):
        return self.title

    def __repr__(self):
        return "<Topic %r>" % self.title

    def pagea(self, page=None):
        per_page = current_app.config['PER_PAGE']
        return self.paginate(page, per_page, True)

    # @staticmethod
    # def page(page):
    #     app = current_app._get_current_object()
    #     per_page = app.config['PER_PAGE']
    #     return Topic.paginate(page, per_page, True)
    def to_json(self):
        data = {
            'id': self.id,
            'uid': self.uid,
            'title': self.uid,
            'tags': self.tags,
            'content': self.content,
            'is_good': self.is_good,
            'is_markdown': self.is_markdown,
            'is_top': self.is_top,
            'publish': self.publish,
            'author':self.author.username
        }


@event.listens_for(Topic, 'before_update')
def receive_after_update(mapper, connection, target):
    target.updated = datetime.now()


class Reply(db.Model):
    __tablename__ = 'replies'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    # quote = db.Column(db.Text, nullable=True)
    publish = db.Column(db.DateTime, default=datetime.now())
    updated = db.Column(db.DateTime)
    topic_id = db.Column(db.Integer,
                         db.ForeignKey('topics.id',
                                       ondelete="CASCADE"))
    topic = db.relationship(
        'Topic',
        backref=db.backref('replies',
                           cascade='all,delete-orphan',
                           lazy='dynamic',
                           order_by='Reply.publish.desc()'))

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User',
                             backref=db.backref('replies',
                                                lazy='dynamic',
                                                order_by='Reply.publish'))
    likers = db.relationship(
        'User',
        secondary='likes',
        backref=db.backref("likes", lazy='dynamic'))
    __mapper_args__ = {"order_by": publish.desc()}


class CollectTopic(db.Model):
    __tablename__ = 'collect_topic'
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    collect_id = db.Column(db.Integer, db.ForeignKey('collects.id'))


class Collect(db.Model):
    __tablename__ = 'collects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(256))
    is_privacy = db.Column(db.Boolean, default=False)
    author_id = db.Column(db.Integer,
                          db.ForeignKey('users.id',
                                        ondelete="CASCADE"))
    author = db.relationship('User',
                             backref=db.backref('collects',
                                                cascade='all,delete-orphan',
                                                lazy='dynamic'))

    topics = db.relationship('Topic',
                             secondary='collect_topic',
                             lazy='dynamic',
                             backref="collects")

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Collect %r>" % self.name


class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    reply_id = db.Column(db.Integer, db.ForeignKey('replies.id'))
    like_time = db.Column(db.DateTime, default=datetime.now())
