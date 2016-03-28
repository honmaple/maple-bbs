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

tag_question = db.Table('tag_question',
                        db.Column('tags_id',
                                  db.Integer,
                                  db.ForeignKey('tags.id',
                                                ondelete="CASCADE")),
                        db.Column('questions_id',
                                  db.Integer,
                                  db.ForeignKey('questions.id',
                                                ondelete="CASCADE")))


class Tags(db.Model):
    __tablename__ = 'tags'
    '''帖子节点'''
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    time = db.Column(db.DateTime, nullable=False)

    __mapper_args__ = {"order_by": time.desc()}

    def __init__(self, name, author):
        self.name = name
        self.author = author
        self.time = datetime.now()

    def __repr__(self):
        return '<Tags %r>' % self.name


class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    kind = db.Column(db.String(60), nullable=True)
    tags = db.relationship('Tags',
                           secondary=tag_question,
                           lazy='dynamic',
                           backref="questions",
                           cascade='all,delete-orphan',
                           single_parent=True,
                           #  passive_deletes=True,
                           order_by='Tags.time.desc()')
    is_good = db.Column(db.Boolean, nullable=False, default=False)
    is_top = db.Column(db.Boolean, nullable=False, default=False)
    is_markdown = db.Column(db.Boolean, nullable=False, default=False)
    is_group = db.Column(db.Boolean, nullable=False, default=False)
    last_author = db.Column(db.String, nullable=False)
    last_time = db.Column(db.DateTime, nullable=False)

    collectors = db.relationship('User',
                                 secondary='collects',
                                 backref=db.backref('collect_questions',
                                                    cascade='all,delete',
                                                    lazy='dynamic'))

    author_id = db.Column(db.Integer, db.ForeignKey('users.id',
                                                    ondelete="CASCADE"))
    author = db.relationship('User',
                             backref=db.backref('questions',
                                                cascade='all,delete-orphan',
                                                lazy='dynamic'))

    group_id = db.Column(db.Integer,
                         db.ForeignKey('groups.id',
                                       ondelete="CASCADE"))
    group = db.relationship('Group',
                            backref=db.backref('questions',
                                               cascade='all,delete-orphan',
                                               lazy='dynamic'))
    board_id = db.Column(db.Integer,
                         db.ForeignKey('board_s.id',
                                       ondelete="CASCADE"))
    board = db.relationship('Board_S',
                            backref=db.backref('questions',
                                               cascade='all,delete-orphan',
                                               lazy='dynamic'))

    __mapper_args__ = {"order_by": time.desc()}

    def __init__(self, title, content, kind):
        self.title = title
        self.content = content
        self.kind = kind
        self.time = datetime.now()
        self.last_author = current_user.name
        self.last_time = datetime.now()

    def __repr__(self):
        return "<Questions %r>" % self.title

    @staticmethod
    def load_by_id(mode):
        return Questions.query.filter_by(id=mode).first_or_404()

    @staticmethod
    def load_by_kind(mode):
        return Questions.query.filter_by(kind=mode).all()


class Replies(db.Model):
    __tablename__ = 'replies'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    quote = db.Column(db.Text, nullable=True)
    time = db.Column(db.DateTime, nullable=False)
    question_id = db.Column(db.Integer,
                            db.ForeignKey('questions.id',
                                          ondelete="CASCADE"))
    question = db.relationship('Questions',
                               backref=db.backref('replies',
                                                  cascade='all,delete-orphan',
                                                  lazy='dynamic',
                                                  order_by='Replies.time'))

    lovers = db.relationship('User',
                             secondary='loves',
                             backref=db.backref('love_replies',
                                                cascade='all,delete',
                                                lazy='dynamic'))

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User',
                             backref=db.backref('replies',
                                                lazy='dynamic',
                                                order_by='Replies.time'))

    __mapper_args__ = {"order_by": time.desc()}

    def __init__(self, content, quote):
        self.content = content
        self.quote = quote
        self.time = datetime.now()

    def __repr__(self):
        return "<Replies %r>" % self.content

    @staticmethod
    def load_by_id(mode):
        return Replies.query.filter_by(id=mode).first()


class Collector(db.Model):
    __tablename__ = 'collects'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id',
                                      ondelete="CASCADE"))
    question_id = db.Column(db.Integer,
                            db.ForeignKey('questions.id',
                                          ondelete="CASCADE"))
    collect_time = db.Column(db.DateTime,
                             default=datetime.now(),
                             nullable=False)

    def __init__(self):
        self.collect_time = datetime.now()

    @staticmethod
    def load_by_id(qid, uid):
        return Collector.query.filter_by(question_id=qid, user_id=uid).first()

    @staticmethod
    def load(qid, uid):
        return Collector.query.filter_by(question_id=qid, user_id=uid).first()


class Lover(db.Model):
    __tablename__ = 'loves'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id',
                                      ondelete="CASCADE"))
    reply_id = db.Column(db.Integer,
                         db.ForeignKey('replies.id',
                                       ondelete="CASCADE"))
    like_time = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    def __init__(self):
        self.like_time = datetime.now()

    @staticmethod
    def load_by_id(rid, uid):
        return Lover.query.filter_by(reply_id=rid, user_id=uid).first()

    @staticmethod
    def load(rid, uid):
        return Lover.query.filter_by(reply_id=rid, user_id=uid).first()
