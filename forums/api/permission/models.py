#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: models.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-17 09:13:38 (CST)
# Last Update:星期六 2016-12-17 9:35:12 (CST)
#          By:
# Description:
# **************************************************************************
from flask_maple.models import db, ModelMixin
from sqlalchemy import event
from sqlalchemy.orm import object_session
from api.user.models import User

group_user = db.Table(
    'group_user',
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')))

group_permission = db.Table(
    'group_permission',
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id')))

router_permission = db.Table(
    'router_permission',
    db.Column('router_id', db.Integer, db.ForeignKey('routers.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id')))


class Permission(db.Model, ModelMixin):
    __tablename__ = 'permissions'

    METHOD_GET = '0'
    METHOD_POST = '1'
    METHOD_PUT = '2'
    METHOD_DELETE = '3'
    METHOD_PATCH = '4'
    METHOD_ALL = '5'

    METHOD = (('0', 'GET 方式'), ('1', 'POST 方式'), ('2', 'PUT 方式'),
              ('3', 'DELETE 方式'), ('4', 'PATCH 方式'), ('5', '所有方式'))

    PERMISSION_DENY = '0'
    PERMISSION_ALLOW = '1'

    PERMISSION = (('0', '禁止'), ('1', '允许'))

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512), nullable=False, unique=True)
    allow = db.Column(db.String(10), nullable=False, default=PERMISSION_ALLOW)
    method = db.Column(db.String(16), nullable=False, default=METHOD_GET)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Permission %r>" % self.name

    def is_allowed(self):
        if self.allow == self.PERMISSION_ALLOW:
            return True
        return False

    def is_denied(self):
        if self.allow == self.PERMISSION_DENY:
            return True
        return False

# class Callback(db.Model, ModelMixin):
#     __tablename__ = 'callbacks'

#     CALLBACK_TYPE_HTTP = '0'
#     CALLBACK_TYPE_JSON = '1'
#     CALLBACK_TYPE_REDIRECT = '2'

#     CALLBACK_TYPE = (('0', '403 Forbidden'), ('1', 'Json'), ('2', 'Redirect'))

#     id = db.Column(db.Integer, primary_key=True)
#     callback = db.Column(db.String(512), nullable=False, unique=True)
#     callback_type = db.Column(
#         db.String(10), nullable=False, default=CALLBACK_TYPE_HTTP)
#     description = db.Column(db.String(128), nullable=True)

#     def __str__(self):
#         return self.callback

#     def __repr__(self):
#         return "<Callback %r>" % self.callback


class Group(db.Model, ModelMixin):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512), nullable=False, unique=True)
    permissions = db.relationship(
        Permission,
        secondary=group_permission,
        backref=db.backref(
            'groups', lazy='dynamic'),
        lazy='dynamic')
    users = db.relationship(
        User,
        secondary=group_user,
        backref=db.backref(
            'groups', lazy='dynamic'),
        lazy='dynamic')

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Group %r>" % self.name

    def get_permissions(self):
        return self.permissions.all()

    def has_perm(self, perm):
        if perm in self.get_permissions():
            return True
        return False

    def has_perms(self, perm_list):
        router_perm_list = set(perm_list)
        group_perm_list = set(self.get_permissions())
        common_perm_list = router_perm_list & group_perm_list
        if not common_perm_list:
            return False
        return True


class Router(db.Model, ModelMixin):
    __tablename__ = 'routers'

    URL_TYPE_HTTP = '0'
    URL_TYPE_ENDPOINT = '1'
    URL_TYPE = (('0', 'HTTP'), ('1', 'Endpoint'))

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(512), nullable=False, unique=True)
    url_type = db.Column(db.String(10), nullable=False, default=URL_TYPE_HTTP)
    description = db.Column(db.String(128), nullable=True)
    # callback_id = db.Column(db.Integer, db.ForeignKey('callbacks.id'))
    # callback = db.relationship(
    #     Callback, backref=db.backref(
    #         'routers', lazy='dynamic'),
    #     lazy='joined')
    permissions = db.relationship(
        Permission,
        secondary=router_permission,
        backref=db.backref(
            'routers', lazy='dynamic'),
        lazy='dynamic')

    def __repr__(self):
        return "<Router %r>" % self.url

    def _get_filter_dict(self, method):
        filter_dict = {}
        if method == "HEAD":
            method = "GET"
        if hasattr(Permission, 'METHOD_' + method):
            filter_dict.update(method=getattr(Permission, 'METHOD_' + method))
        return filter_dict

    def get_permissions(self):
        return self.permissions.all()

    def get_allow_permissions(self):
        return self.permissions.filter_by(
            allow=Permission.PERMISSION_ALLOW).all()

    def get_deny_permissions(self):
        return self.permissions.filter_by(allow=Permission.PERMISSION_DENY)

    def get_method_permissions(self, method):
        filter_dict = self._get_filter_dict(method)
        return self.permissions.filter_by(**filter_dict).all()

    def get_allow_method_permissions(self, method):
        filter_dict = self._get_filter_dict(method)
        filter_dict.update(allow=Permission.PERMISSION_ALLOW)
        return self.permissions.filter_by(**filter_dict).all()

    def get_deny_method_permissions(self, method):
        filter_dict = self._get_filter_dict(method)
        filter_dict.update(allow=Permission.PERMISSION_DENY)
        return self.permissions.filter_by(**filter_dict).all()


@event.listens_for(Group, 'after_insert')
def add_group_permission(mapper, connection, target):
    method_list = ['GET', 'POST', 'PUT', 'DELETE']
    perm_list = []
    for method in method_list:
        name = target.name + '组' + '允许' + method + '请求'
        perm = Permission.query.filter_by(name=name).first()
        if perm is None:
            perm = Permission()
            perm.name = name
            perm.allow = Permission.PERMISSION_ALLOW
            perm.method = getattr(Permission, 'METHOD_' + method)
            object_session(target).add(perm)
        perm_list.append(perm)

        name = target.name + '组' + '禁止' + method + '请求'
        perm = Permission.query.filter_by(name=name).first()
        if perm is None:
            perm = Permission()
            perm.name = name
            perm.allow = Permission.PERMISSION_DENY
            perm.method = getattr(Permission, 'METHOD_' + method)
            object_session(target).add(perm)
        perm_list.append(perm)
    for perm in perm_list:
        target.permissions.append(perm)


@event.listens_for(Group, 'before_delete')
def delete_group_permission(mapper, connection, target):
    method_list = ['GET', 'POST', 'PUT', 'DELETE']
    for method in method_list:
        name = target.name + '组' + '允许' + method + '请求'
        perm = Permission.query.filter_by(
            name=name, allow=Permission.PERMISSION_ALLOW).first()
        if perm is not None:
            object_session(target).delete(perm)

        name = target.name + '组' + '禁止' + method + '请求'
        perm = Permission.query.filter_by(
            name=name, allow=Permission.PERMISSION_DENY).first()
        if perm is not None:
            object_session(target).delete(perm)
