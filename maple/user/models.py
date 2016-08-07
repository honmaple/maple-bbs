#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: models.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 13:24:19 (CST)
# Last Update:星期二 2016-8-2 20:47:53 (CST)
#          By:
# Description:
# **************************************************************************
from maple import db
from maple.tag.models import Tags
from maple.mine.models import Follow
from maple.topic.models import Topic
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import (generate_password_hash, check_password_hash)

__all__ = ['User', 'UserRole', 'Role', 'UserInfor', 'UserSetting', 'OpenID']


class UserRole(db.Model):
    __tablename__ = 'user_role'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    roles_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(49), unique=True)
    email = db.Column(db.String(81), unique=True)
    password = db.Column(db.String, nullable=False)
    is_superuser = db.Column(db.Boolean, default=False)
    is_confirmed = db.Column(db.Boolean, default=False)
    register_time = db.Column(db.DateTime, default=datetime.now())

    following_tags = db.relationship(
        'Tags',
        secondary='follows',
        primaryjoin="User.id==follows.c.follower_id",
        lazy='dynamic',
        backref=db.backref('followers', lazy='dynamic'))
    following_topics = db.relationship(
        'Topic',
        secondary='follows',
        primaryjoin="User.id==follows.c.follower_id",
        lazy='dynamic',
        backref=db.backref('followers', lazy='dynamic'))
    following_collects = db.relationship(
        'Collect',
        secondary='follows',
        primaryjoin="User.id==follows.c.follower_id",
        lazy='dynamic',
        backref=db.backref('followers', lazy='dynamic'))
    following_users = db.relationship(
        'User',
        secondary='follows',
        primaryjoin="User.id==follows.c.follower_id",
        secondaryjoin="User.id==follows.c.following_user_id",
        lazy='dynamic',
        backref=db.backref('followers', lazy='dynamic'), )

    setting_id = db.Column(db.Integer,
                           db.ForeignKey('usersetting.id',
                                         ondelete="CASCADE"))
    setting = db.relationship("UserSetting",
                              backref="user",
                              cascade='all,delete',
                              uselist=False)

    infor_id = db.Column(db.Integer,
                         db.ForeignKey('userinfor.id',
                                       ondelete="CASCADE"))
    infor = db.relationship("UserInfor",
                            backref=db.backref('user', lazy='joined'),
                            cascade='all,delete',
                            uselist=False)

    roles = db.relationship('Role',
                            secondary='user_role',
                            backref=db.backref('users'),
                            lazy='dynamic')

    def __str__(self):
        return self.username

    def __repr__(self):
        return '<User %r>' % self.username

    # @property
    # def password(self):
    #     return "密码不是可读形式!"

    # @password.setter
    # def password(self, password):
    #     self.password_hash = generate_password_hash(password)

    # def verify_password(self, password):
    #     return check_password_hash(password)

    @staticmethod
    def set_password(password):
        pw_hash = generate_password_hash(password)
        return pw_hash

    def check_password(self, password):
        return check_password_hash(self.password, password)



roles_parents = db.Table(
    'roles_parents',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
    db.Column('parent_id', db.Integer, db.ForeignKey('roles.id')))


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(81), nullable=False, default='unconfirmed')
    description = db.Column(db.String(255), nullable=True)
    parents = db.relationship('Role',
                              secondary=roles_parents,
                              primaryjoin=(id == roles_parents.c.role_id),
                              secondaryjoin=(id == roles_parents.c.parent_id),
                              backref=db.backref('children'))

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Role %r>' % self.name


class UserInfor(db.Model):
    __tablename__ = 'userinfor'
    id = db.Column(db.Integer, primary_key=True)
    # confirmed_time = db.Column(db.DateTime, nullable=True)
    # registered_time = db.Column(db.DateTime, nullable=False)
    # score = db.Column(db.Integer, nullable=False, default=100)
    avatar = db.Column(db.String)
    word = db.Column(db.Text, nullable=True)
    introduce = db.Column(db.Text, nullable=True)
    school = db.Column(db.String, nullable=True)

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

# class OpenID(db.Model):
#     __tablename__ = 'openids'
#     id = db.Column(db.Integer, primary_key=True)
#     openid = db.Column(db.Integer, nullable=False)
#     openid_type = db.Column(db.String, nullable=False)
#     nickname = db.Column(db.String, nullable=False)
#     email = db.Column(db.String)
#     avatar = db.Column(db.String)
#     user_id = db.Column(db.Integer,
#                         db.ForeignKey('users.id',
#                                       ondelete="CASCADE"))
#     user = db.relationship('User',
#                            backref=db.backref('openids',
#                                               cascade='all,delete-orphan',
#                                               lazy='dynamic'))

from . import events
