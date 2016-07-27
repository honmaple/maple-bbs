#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: models.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-07-20 17:00:08 (CST)
# Last Update:星期四 2016-7-28 22:30:37 (CST)
#          By:
# Description:
# **************************************************************************
from maple import db
from datetime import datetime

tag_topic = db.Table('tag_topic', db.Column('tags_id', db.Integer,
                                            db.ForeignKey('tags.id')),
                     db.Column('topics_id', db.Integer,
                               db.ForeignKey('topics.id')))

tags_parents = db.Table(
    'tags_parents', db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('parent_id', db.Integer, db.ForeignKey('tags.id')))


class Tags(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=datetime.utcnow())
    tagname = db.Column(db.String(64), nullable=False)
    summary = db.Column(db.Text)
    tags = db.relationship('Topic',
                           secondary=tag_topic,
                           lazy='dynamic',
                           backref="tags")
    parents = db.relationship(
        'Tags',
        secondary=tags_parents,
        primaryjoin=(id == tags_parents.c.tag_id),
        secondaryjoin=(id == tags_parents.c.parent_id),
        backref=db.backref('children', lazy='joined'))

    def __str__(self):
        return self.tagname

    def __repr__(self):
        return '<Tags %r>' % self.tagname
