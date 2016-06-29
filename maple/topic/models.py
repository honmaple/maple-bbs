#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: models.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 13:32:12 (CST)
# Last Update:星期二 2016-6-28 11:53:41 (CST)
#          By:
# Description:
# **************************************************************************
from maple import db
from datetime import datetime
from sqlalchemy import event

tag_topic = db.Table('tag_topic', db.Column('tags_id', db.Integer,
                                            db.ForeignKey('tags.id')),
                     db.Column('topics_id', db.Integer,
                               db.ForeignKey('topics.id')))


class Tags(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tagname = db.Column(db.String(64), nullable=False)
    summary = db.Column(db.Text)

    def __str__(self):
        return self.tagname

    def __repr__(self):
        return '<Tags %r>' % self.tagname


class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(36), nullable=False)
    title = db.Column(db.String(81), nullable=False)
    content = db.Column(db.Text, nullable=False)
    publish = db.Column(db.DateTime, default=datetime.now())
    updated = db.Column(db.DateTime)
    vote = db.Column(db.Integer, default=0)

    tags = db.relationship('Tags',
                           secondary=tag_topic,
                           lazy='dynamic',
                           backref="topics", )

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
    topic = db.relationship('Topic',
                            backref=db.backref('replies',
                                               cascade='all,delete-orphan',
                                               lazy='dynamic',
                                               order_by='Reply.publish'))

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User',
                             backref=db.backref('replies',
                                                lazy='dynamic',
                                                order_by='Reply.publish'))
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

# class TopicCount(db.Model):
#     __tablename__ = 'topic_counts'
#     id = db.Column(db.Integer, primary_key=True)
#     topic_id = db.Column(db.Integer,
#                          db.ForeignKey('topics.id',
#                                        ondelete="CASCADE"))
#     topic = db.relationship("Topic",
#                             backref="counts",
#                             cascade='all,delete-orphan',
#                             single_parent=True,
#                             uselist=False)
#     read = db.Column(db.Integer, default=0)
#     reply = db.Column(db.Integer, default=0)
#     vote = db.Column(db.Integer, default=0)

#     def __repr__(self):
#         return '<TopicCount %r>' % self.id
