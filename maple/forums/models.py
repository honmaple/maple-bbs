#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: models.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 13:24:19 (CST)
# Last Update:星期六 2016-7-23 20:58:12 (CST)
#          By:
# Description:
# **************************************************************************
from maple import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON


class Board(db.Model):
    __tablename__ = 'boards'
    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.Integer, default=1)
    board = db.Column(db.String(81), nullable=False)
    parent_board = db.Column(db.String(81), nullable=False)
    description = db.Column(db.Text(), nullable=False)

    count_id = db.Column(db.Integer,
                         db.ForeignKey('counts.id',
                                       ondelete="CASCADE"))
    count = db.relationship('Count',
                            backref="board",
                            cascade='all,delete-orphan',
                            single_parent=True,
                            uselist=False)

    __mapper_args__ = {"order_by": rank.desc()}

    def __str__(self):
        return self.board

    def __repr__(self):
        return '<Board %r>' % self.board


class Count(db.Model):
    __tablename__ = 'counts'
    id = db.Column(db.Integer, primary_key=True)
    drafts = db.Column(db.Integer, default=0)
    collects = db.Column(db.Integer, default=0)
    inviteds = db.Column(db.Integer, default=0)
    follows = db.Column(db.Integer, default=0)
    topics = db.Column(db.Integer, default=0)
    all_topics = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Count %r>' % self.id


class Notice(db.Model):
    __tablename__ = 'notices'
    id = db.Column(db.Integer, primary_key=True)
    publish = db.Column(db.DateTime, default=datetime.now())
    category = db.Column(db.String(81), nullable=False)
    content = db.Column(JSON)
    is_read = db.Column(db.Boolean, default=False)

    rece_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    rece_user = db.relationship("User",
                                backref="rece_user",
                                foreign_keys='Notice.rece_id',
                                uselist=False)

    send_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    send_user = db.relationship("User",
                                backref="send_user",
                                foreign_keys='Notice.send_id',
                                uselist=False)

    def __repr__(self):
        return '<Notice %r>' % self.id
