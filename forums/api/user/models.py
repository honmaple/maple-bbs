#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: models.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-15 21:09:08 (CST)
# Last Update: Wednesday 2018-07-25 18:54:54 (CST)
#          By:
# Description:
# **************************************************************************
from datetime import datetime, timedelta

from flask import current_app
from flask_babel import lazy_gettext as _
from flask_login import current_user, login_user, logout_user
from flask_principal import Identity, identity_changed, AnonymousIdentity
from pytz import all_timezones
from sqlalchemy import event
from sqlalchemy.orm import object_session
from flask_maple.models import ModelMixin
from flask_maple.auth.models import UserMixin, GroupMixin
from flask_maple.permission.models import PermissionMixin
from forums.common.records import load_online_sign_users
from forums.count import Count
from forums.extension import db, mail

user_follower = db.Table(
    'user_follower',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')))


class Permission(db.Model, PermissionMixin):
    __tablename__ = 'permission'


class Group(db.Model, GroupMixin):
    __tablename__ = 'group'


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)

    followers = db.relationship(
        'User',
        secondary=user_follower,
        primaryjoin=(id == user_follower.c.user_id),
        secondaryjoin=(id == user_follower.c.follower_id),
        backref=db.backref(
            'following_users', lazy='dynamic'),
        lazy='dynamic')

    def is_followed(self, user=None):
        if user is None:
            user = current_user
        return db.session.query(user_follower).filter(
            user_follower.c.user_id == self.id,
            user_follower.c.follower_id == user.id).exists()

    def login(self, remember=True):
        login_user(self, remember)
        identity_changed.send(
            current_app._get_current_object(), identity=Identity(self.id))

    def logout(self):
        logout_user()
        identity_changed.send(
            current_app._get_current_object(), identity=AnonymousIdentity())

    @property
    def is_not_confirmed(self):
        return (not self.is_confirmed and self.id == current_user.id)

    @property
    def is_online(self):
        setting = self.setting
        if setting.online_status == UserSetting.STATUS_ALLOW_ALL:
            return self.username in load_online_sign_users()
        elif setting.online_status == UserSetting.STATUS_ALLOW_AUTHENTICATED:
            return self.username in load_online_sign_users(
            ) and current_user.is_authenticated
        elif setting.online_status == UserSetting.STATUS_ALLOW_OWN:
            return current_user.id == self.id
        return False

    @property
    def topic_count(self):
        return self.topics.count()

    @topic_count.setter
    def topic_count(self, value):
        return Count.user_topic_count(self.id, value)

    @property
    def reply_count(self):
        return self.replies.count()

    @reply_count.setter
    def reply_count(self, value):
        return Count.user_reply_count(self.id, value)

    @property
    def message_count(self):
        # return self.receive_messages.filter_by(status='0').count()
        return Count.user_message_count(self.id)

    @message_count.setter
    def message_count(self, value):
        return Count.user_message_count(self.id, value)

    @property
    def send_email_time(self):
        # return self.receive_messages.filter_by(status='0').count()
        return Count.user_email_time(self.id)

    @send_email_time.setter
    def send_email_time(self, value):
        return Count.user_email_time(self.id, value)

    @property
    def email_is_allowed(self):
        t = self.send_email_time
        t = datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
        now = datetime.now()
        if t + timedelta(hours=3) < now:
            self.send_email_time = now.strftime('%Y-%m-%d %H:%M:%S')
            return True
        return False

    def send_email(self, *args, **kwargs):
        kwargs.update(recipients=[self.email])
        mail.send_email(*args, **kwargs)

    def send_email_to_admin(self):
        ''''
        When someone registered an account,send email to admin.
        '''
        recipients = current_app.config['RECEIVER']
        subject = '{} has registered an account.'.format(self.username)
        html = '<p>username: {}</p><p>email: {}</p>'.format(self.username,
                                                            self.email)
        mail.send_email(subject=subject, html=html, recipients=recipients)


class UserInfo(db.Model, ModelMixin):
    __tablename__ = 'userinfo'
    id = db.Column(db.Integer, primary_key=True)
    avatar = db.Column(db.String(128))
    school = db.Column(db.String(128), nullable=True)
    word = db.Column(db.Text, nullable=True)
    introduce = db.Column(db.Text, nullable=True)

    user_id = db.Column(
        db.Integer, db.ForeignKey(
            'user.id', ondelete="CASCADE"))
    user = db.relationship(
        User,
        backref=db.backref(
            "info", uselist=False, cascade='all,delete', lazy='joined'),
        uselist=False,
        lazy='joined')

    def __repr__(self):
        return "<UserInfo %r>" % str(self.id)

    def __str__(self):
        return "%s's info" % self.user_id


class UserSetting(db.Model, ModelMixin):
    STATUS_ALLOW_ALL = '0'
    STATUS_ALLOW_AUTHENTICATED = '1'
    STATUS_ALLOW_OWN = '2'

    STATUS = (('0', _('ALLOW ALL USER')), ('1', _('ALLOW AUTHENTICATED USER')),
              ('2', _('ALLOW OWN')))

    LOCALE_CHINESE = 'zh'
    LOCALE_ENGLISH = 'en'
    LOCALE = (('zh', _('Chinese')), ('en', _('English')))

    TIMEZONE_UTC = 'UTC'
    TIMEZONE = [(i, i) for i in all_timezones]

    __tablename__ = 'usersetting'
    id = db.Column(db.Integer, primary_key=True)
    online_status = db.Column(
        db.String(10), nullable=False, default=STATUS_ALLOW_ALL)
    topic_list = db.Column(
        db.String(10), nullable=False, default=STATUS_ALLOW_ALL)
    rep_list = db.Column(
        db.String(10), nullable=False, default=STATUS_ALLOW_ALL)
    ntb_list = db.Column(
        db.String(10), nullable=False, default=STATUS_ALLOW_OWN)
    collect_list = db.Column(
        db.String(10), nullable=False, default=STATUS_ALLOW_AUTHENTICATED)
    locale = db.Column(db.String(32), nullable=False, default=LOCALE_CHINESE)
    timezone = db.Column(db.String(32), nullable=False, default=TIMEZONE_UTC)

    user_id = db.Column(
        db.Integer, db.ForeignKey(
            'user.id', ondelete="CASCADE"))
    user = db.relationship(
        User,
        backref=db.backref(
            "setting", uselist=False, cascade='all,delete', lazy='joined'),
        uselist=False,
        lazy='joined')

    def __repr__(self):
        return "<UserSetting %r>" % str(self.id)

    def __str__(self):
        return "%s's setting" % self.user_id


@event.listens_for(User, 'before_insert')
def add_info(mapper, connection, target):
    info = UserInfo()
    setting = UserSetting()
    object_session(target).add(info)
    object_session(target).add(setting)
    target.info = info
    target.setting = setting
