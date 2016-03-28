#!/usr/bin/env python
# -*- coding=UTF-8 -*-
#*************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: config_db.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2016-03-13 20:36:05
#*************************************************************************
from maple import db


class Board_F(db.Model):
    __tablename__ = 'board_f'
    id = db.Column(db.Integer, primary_key=True)
    chname_f = db.Column(db.String, nullable=False)
    enname_f = db.Column(db.String, nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    count_id = db.Column(db.Integer,
                            db.ForeignKey('counts.id',
                                          ondelete="CASCADE"))
    count = db.relationship("Counts",
                               backref="board_f",
                               cascade='all,delete-orphan',
                               single_parent=True,
                               uselist=False)


    __mapper_args__ = {
        "order_by": rank
    }
    def __init__(self, chname_f, enname_f,rank):
        self.chname_f = chname_f
        self.enname_f = enname_f
        self.rank = rank

    def __repr__(self):
        return "<Board_F %r>" % self.id

    @staticmethod
    def load_all():
        return Board_F.query.all()

    @staticmethod
    def load_by_id(bid):
        return Board_F.query.filter_by(id=bid).first_or_404()

    @staticmethod
    def load_by_name(name):
        return Board_F.query.filter_by(enname_f=name).first_or_404()


class Board_S(db.Model):
    __tablename__ = 'board_s'
    id = db.Column(db.Integer, primary_key=True)
    chname_s = db.Column(db.String, nullable=False)
    enname_s = db.Column(db.String, nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('board_f.id',
                                                   ondelete="CASCADE"))
    board_f = db.relationship('Board_F',
                              backref=db.backref('board_s',
                                                 cascade='all,delete-orphan',
                                                 lazy='dynamic'))
    count_id = db.Column(db.Integer,
                            db.ForeignKey('counts.id',
                                          ondelete="CASCADE"))
    count = db.relationship("Counts",
                               backref="board_s",
                               cascade='all,delete-orphan',
                               single_parent=True,
                               uselist=False)

    __mapper_args__ = {
        "order_by": enname_s
    }

    def __init__(self, chname_s, enname_s):
        self.chname_s = chname_s
        self.enname_s = enname_s

    def __repr__(self):
        return "<Board_S %r>" % self.id

    @staticmethod
    def load_by_name(name):
        return Board_S.query.filter_by(enname_s=name).first_or_404()

    @staticmethod
    def load_by_id(bid):
        return Board_S.query.filter_by(id=bid).first_or_404()
