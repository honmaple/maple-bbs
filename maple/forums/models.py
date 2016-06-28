#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: models.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 13:24:19 (CST)
# Last Update:星期二 2016-6-28 1:4:23 (CST)
#          By:
# Description:
# **************************************************************************
from maple import db
from datetime import datetime


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
    # author_id = db.Column(db.Integer,
    #                       db.ForeignKey('users.id',
    #                                     ondelete="CASCADE"))
    # author = db.relationship("User",
    #                          backref="counts",
    #                          cascade='all,delete-orphan',
    #                          single_parent=True,
    #                          uselist=False)
    drafts = db.Column(db.Integer, default=0)
    collects = db.Column(db.Integer, default=0)
    inviteds = db.Column(db.Integer, default=0)
    follows = db.Column(db.Integer, default=0)
    topics = db.Column(db.Integer, default=0)
    all_topics = db.Column(db.Integer, default=0)

    # board_id = db.Column(db.Integer,
    #                      db.ForeignKey(Board.id,
    #                                    ondelete="CASCADE"))
    # board = db.relationship(Board,
    #                         backref=db.backref("count", lazy="dynamic"),
    #                         cascade='all,delete-orphan',
    #                         single_parent=True,
    #                         uselist=False)

    def __repr__(self):
        return '<Count %r>' % self.id


class Notice(db.Model):
    __tablename__ = 'notices'
    id = db.Column(db.Integer, primary_key=True)
    publish = db.Column(db.DateTime, default=datetime.now())
    category = db.Column(db.String(81), nullable=False)
    content = db.Column(db.Text)

    rece_id = db.Column(db.Integer,
                        db.ForeignKey('users.id',
                                      ondelete="CASCADE"))
    rece_user = db.relationship("User",
                                backref="rece_user",
                                foreign_keys='Notice.rece_id',
                                cascade='all,delete-orphan',
                                single_parent=True,
                                uselist=False)

    send_id = db.Column(db.Integer,
                        db.ForeignKey('users.id',
                                      ondelete="CASCADE"))
    send_user = db.relationship("User",
                                backref="send_user",
                                foreign_keys='Notice.send_id',
                                cascade='all,delete-orphan',
                                single_parent=True,
                                uselist=False)

    def __repr__(self):
        return '<Notice %r>' % self.id
