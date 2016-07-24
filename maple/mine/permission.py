#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: permission.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-07-16 17:18:48 (CST)
# Last Update:星期日 2016-7-24 12:57:59 (CST)
#          By:
# Description:
# **************************************************************************
from flask import (url_for, jsonify, g, flash, redirect, request, abort)
from flask_login import login_required
from flask_principal import Permission
from maple.permission.base import RestBase
from maple.permission.permission import GetCollect, PostCollect


class FollowPermission(RestBase):
    decorators = [login_required]

    def get(self, type):
        if type is not None:
            type_list = ['tag', 'topic', 'user', 'collect']
            if type not in type_list:
                return True

    def put(self, type):
        return True

    def post(self, type):
        type_list = ['tag', 'topic', 'user', 'collect']
        if type not in type_list:
            return True

    def delete(self, type):
        type_list = ['tag', 'topic', 'user', 'collect']
        if type not in type_list:
            return True


class CollectPermission(RestBase):
    decorators = [login_required]

    def put(self, collectId):
        permission = Permission(GetCollect(collectId))
        if not permission.can():
            return True

    def delete(self, collectId):
        permission = Permission(GetCollect(collectId))
        if not permission.can():
            return True

    def callback(self):
        flash('你没有权限', 'warning')
        return redirect(url_for('forums.index'))


class CollectDetailPermission(RestBase):
    decorators = [login_required]

    def get(self, collectId):
        if collectId is not None:
            permission = Permission(GetCollect(collectId))
            if not permission.can():
                return True

    def post(self):
        form = request.form.getlist('add-to-collect')
        for collectId in form:
            try:
                collectId = int(collectId)
                permission = Permission(PostCollect(collectId))
                if not permission.can():
                    return True
            except ValueError:
                abort(403)

    def put(self, collectId):
        permission = Permission(GetCollect(collectId))
        if not permission.can():
            return True

    def delete(self, collectId):
        permission = Permission(GetCollect(collectId))
        if not permission.can():
            return True

    def callback(self):
        flash('你没有权限', 'warning')
        return redirect(url_for('mine.collect'))


class LikePermission(RestBase):
    def post(self, replyId):
        if not g.user.is_authenticated:
            return jsonify(judge=False, url=url_for('auth.login'))

    def delete(self, replyId):
        if not g.user.is_authenticated:
            return jsonify(judge=False, url=url_for('auth.login'))


follow_permission = FollowPermission()
collect_permission = CollectPermission()
like_permission = LikePermission()
collect_detail_permission = CollectDetailPermission()
