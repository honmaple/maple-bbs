#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: models.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-03-25 18:48:33 (CST)
# Last Update:星期三 2017-3-29 22:14:49 (CST)
#          By:
# Description:
# **************************************************************************
from flask_maple.models import ModelMixin
from forums.extension import db
from forums.count import Count


class Board(db.Model, ModelMixin):
    __tablename__ = 'boards'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(81), nullable=False)
    description = db.Column(db.String(128), nullable=False)
    parent_id = db.Column(
        db.Integer, db.ForeignKey(
            'boards.id', ondelete="CASCADE"))
    parent = db.relationship(
        'Board',
        remote_side=[id],
        backref=db.backref(
            'children',
            remote_side=[parent_id],
            cascade='all,delete-orphan',
            lazy='dynamic'),
        lazy='joined',
        uselist=False)

    @property
    def newest_topic(self):
        return self.topics.order_by('-id').first()

    @property
    def topic_count(self):
        return self.topics.count()

    @topic_count.setter
    def topic_count(self, value):
        Count.board_topic_count(self.id, value)

    @property
    def post_count(self):
        return Count.board_post_count(self.id)

    @post_count.setter
    def post_count(self, value):
        Count.board_post_count(self.id, value)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Board %r>' % self.name
