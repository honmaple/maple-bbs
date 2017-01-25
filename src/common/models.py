#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: models.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-01-25 21:33:09 (CST)
# Last Update:星期三 2017-1-25 21:33:42 (CST)
#          By:
# Description:
# **************************************************************************
from forums.extension import db
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime
from flask_maple.models import ModelMixin


class CommonMixin(ModelMixin):
    @declared_attr
    def id(cls):
        return db.Column(db.Integer, primary_key=True)


class CommonTimeMixin(CommonMixin):
    @declared_attr
    def created_at(cls):
        return db.Column(db.DateTime, default=datetime.utcnow())

    @declared_attr
    def updated_at(cls):
        return db.Column(
            db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())


class CommonUserMixin(CommonTimeMixin):
    @declared_attr
    def user_id(cls):
        return db.Column(
            db.Integer, db.ForeignKey(
                'user.id', ondelete="CASCADE"))

    @declared_attr
    def user(cls):
        name = cls.__name__.lower()
        if not name.endswith('s'):
            name = name + 's'
        if hasattr(cls, 'user_related_name'):
            name = cls.user_related_name
        return db.relationship(
            'User',
            backref=db.backref(
                name, cascade='all,delete', lazy='dynamic'),
            uselist=False,
            lazy='joined')
