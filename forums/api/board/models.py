#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: models.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-13 23:28:30 (CST)
# Last Update:星期日 2016-12-18 19:17:23 (CST)
#          By:
# Description:
# **************************************************************************
from flask_maple.models import ModelMixin
from maple.extension import db

board_parents = db.Table(
    'board_parents',
    db.Column('board_id', db.Integer, db.ForeignKey('boards.id')),
    db.Column('parent_id', db.Integer, db.ForeignKey('boards.id')))


class Board(db.Model, ModelMixin):
    __tablename__ = 'boards'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(81), nullable=False)
    description = db.Column(db.Text(128), nullable=False)
    parent_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'boards.id', ondelete="CASCADE"))
    parent = db.relationship(
        'Board',
        remote_side=[id],
        backref=db.backref(
            'children', cascade='all,delete-orphan', lazy='dynamic'),
        lazy='joined',
        uselist=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Board %r>' % self.name
