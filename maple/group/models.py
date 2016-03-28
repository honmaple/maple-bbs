#*************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: articledb.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2015-11-29 02:07:53
#*************************************************************************
#!/usr/bin/env python
# -*- coding=UTF-8 -*-
from maple import db
from datetime import datetime
from flask_login import current_user


class UserGroup(db.Model):
    __tablename__ = 'usergroups'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    join_time = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    @staticmethod
    def load_join_time(uid, gid):
        time = UserGroup.query.filter_by(user_id=uid,
                                         group_id=gid).first_or_404()
        return time


class Group(db.Model):
    '''
    join_mode:
        1:allow anybody
        2:need validata
        3:not allow anybody
    '''
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    kind = db.Column(db.String, nullable=False)
    join_mode = db.Column(db.Integer, nullable=False, default=2)
    create_time = db.Column(db.DateTime, nullable=False)
    create_author = db.Column(db.String, nullable=False)
    admin = db.Column(db.String, nullable=False)
    introduce = db.Column(db.Text, nullable=False)
    permission = db.Column(db.Integer,nullable=False,default=1)
    users = db.relationship('User',
                            secondary='usergroups',
                            backref=db.backref('groups',
                                               lazy='dynamic'))

    count_id = db.Column(db.Integer,
                            db.ForeignKey('counts.id',
                                          ondelete="CASCADE"))
    count = db.relationship("Counts",
                               backref="group",
                               cascade='all,delete-orphan',
                               single_parent=True,
                               uselist=False)

    def __init__(self, kind, name, introduce):
        self.kind = kind
        self.name = name
        self.introduce = introduce
        self.create_time = datetime.now()
        self.create_author = current_user.name
        self.admin = self.create_author

    def __repr__(self):
        return "<Group %r>" % self.name

    @staticmethod
    def load_all():
        return Group.query.all()

    @staticmethod
    def load_by_id(uid):
        return Group.query.filter_by(id=uid).first_or_404()

    @staticmethod
    def load_by_kind(kind):
        return Group.query.filter_by(kind=kind).all()

    @staticmethod
    def load_by_name(name):
        return Group.query.filter_by(name=name).first_or_404()


class Message(db.Model):
    '''消息提醒功能设计'''
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    send_user = db.Column(db.String, nullable=False)
    rece_user = db.Column(db.String, nullable=False)
    kind = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=True)
    reply_id = db.Column(db.Integer,
                         db.ForeignKey('replies.id',
                                       ondelete="CASCADE"))
    reply = db.relationship("Replies",
                            backref="message",
                            cascade='all,delete-orphan',
                            single_parent=True,
                            uselist=False)
    question_id = db.Column(db.Integer,
                            db.ForeignKey('questions.id',
                                          ondelete="CASCADE"))
    question = db.relationship("Questions",
                               backref="message",
                               cascade='all,delete-orphan',
                               single_parent=True,
                               uselist=False)
    create_time = db.Column(db.DateTime, nullable=False)
    is_read = db.Column(db.Boolean, nullable=False, default=False)
    count = db.Column(db.Integer, nullable=False, default=0)

    __mapper_args__ = {"order_by": create_time.desc()}

    def __init__(self, send_user, rece_user, content, kind):
        self.send_user = send_user
        self.rece_user = rece_user
        self.content = content
        self.kind = kind
        self.create_time = datetime.now()

    def __repr__(self):
        return "<Message %r>" % self.id


class Counts(db.Model):
    __tablename__ = 'counts'
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.Integer, nullable=False, default=0)
    all_topic = db.Column(db.Integer, nullable=False, default=0)
