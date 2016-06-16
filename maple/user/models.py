#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: models.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 13:24:19 (CST)
# Last Update:星期四 2016-6-16 18:17:47 (CST)
#          By:
# Description:
# **************************************************************************
from maple import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, \
    check_password_hash


class UserRole(db.Model):
    __tablename__ = 'user_role'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    roles_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


class Follow(db.Model):
    __tablename__ = 'follows'
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer,
                            db.ForeignKey('users.id'))
    following_user_id = db.Column(db.Integer,
                                  db.ForeignKey('users.id'))
    following_tag_id = db.Column(db.Integer,
                                 db.ForeignKey('tags.id',
                                               ondelete="CASCADE"))
    following_collect_id = db.Column(db.Integer,
                                     db.ForeignKey('collects.id',
                                                   ondelete="CASCADE"))
    followinf_topic_id = db.Column(db.Integer,
                                   db.ForeignKey('topics.id',
                                                 ondelete="CASCADE"))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(49), unique=True)
    email = db.Column(db.String(81), unique=True)
    password = db.Column(db.String, nullable=False)
    is_superuser = db.Column(db.Boolean, default=False)
    is_confirmed = db.Column(db.Boolean, default=False)
    register_time = db.Column(db.DateTime, default=datetime.now())

    likes = db.relationship('Reply',
                            secondary='likes',
                            lazy='dynamic',
                            backref="likers"
                            )
    following_tags = db.relationship('Tags',
                                     secondary='follows',
                                     primaryjoin="User.id==follows.c.follower_id",
                                     lazy='dynamic',
                                     backref="followers",
                                     # cascade='all,delete-orphan',
                                     # single_parent=True,
                                     )
    following_topics = db.relationship('Topic',
                                       secondary='follows',
                                       primaryjoin="User.id==follows.c.follower_id",
                                       lazy='dynamic',
                                       backref="followers",
                                       # cascade='all,delete-orphan',
                                       # single_parent=True,
                                       )
    following_collects = db.relationship('Collect',
                                         secondary='follows',
                                         primaryjoin="User.id==follows.c.follower_id",
                                         lazy='dynamic',
                                         backref="followers",
                                         # cascade='all,delete-orphan',
                                         # single_parent=True,
                                         )
    following_users = db.relationship('User',
                                      secondary='follows',
                                      primaryjoin="User.id==follows.c.follower_id",
                                      secondaryjoin="User.id==follows.c.following_user_id",
                                      backref=db.backref(
                                          'followers', lazy='dynamic'),
                                      lazy='dynamic'
                                      )

    setting_id = db.Column(db.Integer,
                           db.ForeignKey('usersetting.id',
                                         ondelete="CASCADE"))
    setting = db.relationship("UserSetting",
                              backref="users",
                              cascade='all,delete',
                              uselist=False)

    infor_id = db.Column(db.Integer,
                         db.ForeignKey('userinfor.id',
                                       ondelete="CASCADE"))
    infor = db.relationship("UserInfor",
                            backref="users",
                            cascade='all,delete',
                            uselist=False)

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def set_password(password):
        pw_hash = generate_password_hash(password)
        return pw_hash

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(81), nullable=False, default='unconfirmed')
    description = db.Column(db.String(255), nullable=True)
    users = db.relationship('User',
                            secondary='user_role',
                            backref=db.backref('roles', lazy='dynamic'))


class UserInfor(db.Model):
    __tablename__ = 'userinfor'
    id = db.Column(db.Integer, primary_key=True)
    # confirmed_time = db.Column(db.DateTime, nullable=True)
    # registered_time = db.Column(db.DateTime, nullable=False)
    # score = db.Column(db.Integer, nullable=False, default=100)
    word = db.Column(db.Text, nullable=True)
    introduce = db.Column(db.Text, nullable=True)
    school = db.Column(db.String, nullable=True)

    # def __init__(self):
    #     self.registered_time = datetime.now()

    def __repr__(self):
        return "<UserInfor %r>" % self.id


class UserSetting(db.Model):
    '''
    1:all user
    2:logined user
    3:only own
    '''
    __tablename__ = 'usersetting'
    id = db.Column(db.Integer, primary_key=True)
    online_status = db.Column(db.Integer, nullable=False, default=1)
    topic_list = db.Column(db.Integer, nullable=False, default=1)
    rep_list = db.Column(db.Integer, nullable=False, default=1)
    ntb_list = db.Column(db.Integer, nullable=False, default=3)
    collect_list = db.Column(db.Integer, nullable=False, default=2)
    locale = db.Column(db.String(32), default='zh')
    timezone = db.Column(db.String(32), default='UTC')

    def __repr__(self):
        return "<UserSetting %r>" % self.id


class OpenID(db.Model):
    __tablename__ = 'openids'
    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.Integer, nullable=False)
    openid_type = db.Column(db.String, nullable=False)
    nickname = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    avatar = db.Column(db.String)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id',
                                      ondelete="CASCADE"))
    user = db.relationship('User',
                           backref=db.backref('openids',
                                              cascade='all,delete-orphan',
                                              lazy='dynamic'))

# class Invite(db.Model):
#     __tablename__ = 'invites'
#     id = db.Column(db.Integer, primary_key=True)
#     invite_id = db.Column(db.Integer,
#                           db.ForeignKey('users.id',
#                                         ondelete="CASCADE"))

#     invite = db.relationship("User",
#                              uselist=False,
#                              foreign_keys='Invite.invite_id',
#                              backref="invited"
#                              )

#     invited_id = db.Column(db.Integer,
#                            db.ForeignKey('users.id',
#                                          ondelete="CASCADE"))

#     invited = db.relationship("User",
#                               uselist=False,
#                               foreign_keys='Invite.invited_id',
#                               backref="invite"
#                               )

#     topic_id = db.Column(db.Integer,
#                          db.ForeignKey('topics.id',
#                                        ondelete="CASCADE"))
#     topic = db.relationship("Topic",
#                             uselist=False,
#                             backref="invited"
#                             )
