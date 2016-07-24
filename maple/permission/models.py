#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: models.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-07-24 15:10:52 (CST)
# Last Update:星期日 2016-7-24 15:11:46 (CST)
#          By:
# Description:
# **************************************************************************
from maple import db
from maple.tag.models import Tags
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import (generate_password_hash, check_password_hash)
from sqlalchemy import event

roles_permissions = db.Table(
    'roles_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id')))

routes_permissions = db.Table(
    'routes_permissions',
    db.Column('route_id', db.Integer, db.ForeignKey('routes.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id')))


class Route(db.Model):
    __tablename__ = 'routes'
    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String(256), nullable=False)
    rule = db.Column(db.String(512), nullable=False)
    permissions = db.relationship('Permiss',
                                  secondary=routes_permissions,
                                  backref=db.backref('routes'))

    def __str__(self):
        return "<%s : %s>" % (self.endpoint, self.rule)

    def __repr__(self):
        return "<Route %r>" % self.endpoint


class Permiss(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512), nullable=False)
    is_allow = db.Column(db.Boolean, default=True)
    method = db.Column(db.String(16), nullable=False)
    roles = db.relationship('Role',
                            secondary=roles_permissions,
                            backref=db.backref('permissions'))

    def __str__(self):
        if self.is_allow:
            return self.name + '允许' + self.method
        else:
            return self.name + '禁止' + self.method

    def __repr__(self):
        return "<Permiss %r>" % self.id
