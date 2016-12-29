#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-15 22:08:06 (CST)
# Last Update:星期四 2016-12-29 21:18:30 (CST)
#          By:
# Description:
# **************************************************************************
from flask import render_template, redirect, url_for
from flask.views import MethodView
from flask_maple.serializer import FlaskSerializer as Serializer
from flask_maple.response import HTTPResponse
from common.views import ViewListMixin
from .models import User


class UserListView(MethodView, ViewListMixin):
    def get(self):
        page, number = self.page_info
        users = User.get_list(page, number)
        return render_template('user/user_list.html', users=users)
        # serializer = Serializer(users, many=True)
        # return HTTPResponse(HTTPResponse.NORMAL_STATUS,
        #                     **serializer.data).to_response()

    def post(self):
        return 'post'


class UserView(MethodView):
    def get(self, username):
        return redirect(url_for('mine.topiclist'))
        user = User.get(username=username)
        return render_template('user/user.html', user=user)
        # serializer = Serializer(user, many=False)
        # return HTTPResponse(
        #     HTTPResponse.NORMAL_STATUS, data=serializer.data).to_response()

    def put(self, username):
        return 'put'

    def delete(self, username):
        return 'delete'


class UserFollowView(MethodView):
    pass
