#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from datetime import datetime


class Assert(object):
    def __init__(self, data=dict(), fields=[]):
        self.data = data
        self.fields = fields
        self._asserts = [i for i in dir(self) if i.startswith('assert_')]
        self.init()

    def abort(self, key, value, message):
        print(key, value, message)

    def init(self):
        for m in self._asserts:
            key = m.split("_")[1]
            value = self.data.get(key)
            try:
                getattr(self, m)(self.data.get(key))
            except AssertionError as e:
                return self.abort(key, value, e)

    def or_(self, *args):
        for m in args:
            if callable(m):
                m = m()
            if not m:
                continue
            return True
        return False

    def and_(self, *args):
        for m in args:
            if callable(m):
                m = m()
            if not m:
                return False
        return True

    def require(self, key):
        return bool(key)

    def in_(self, key, value):
        return key in value

    def type_(self, key, value):
        if key is None:
            return False
        return isinstance(key, value)

    def equal(self, key, value, ignore_case=False):
        if callable(value):
            return value(key)
        if ignore_case:
            return key.lower() == value.lower()
        return key == value

    def length(self, key, value):
        if key is None:
            key = ""
        length = len(key)
        if callable(value):
            return value(length)
        return length == value

    def url(self, value):
        key = r'^[a-z]+://(?P<host>[^/:]+)(?P<port>:[0-9]+)?(?P<path>\/.*)?$'
        return self.regex(value, key)

    def email(self, value):
        key = r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$'
        return self.regex(value, key)

    def regex(self, key, value):
        return re.match(value, key)


def update_maybe(ins, request_data, columns):
    for column in columns:
        value = request_data.get(column)
        if value:
            setattr(ins, column, value)
    return ins


def filter_maybe(request_data, columns, params=None):
    if params is None:
        params = dict()
    is_dict = isinstance(columns, dict)
    for column in columns:
        value = request_data.get(column)
        if not value:
            continue
        key = column if not is_dict else columns.get(column, column)

        if key in ["created_at__gte", "created_at__lte"]:
            value = datetime.strptime(value, '%Y-%m-%d')
        params.update({key: value})
    return params


def orderby_maybe(request_data=dict(), keys=[], date_key=False):
    keys.append('id')
    if date_key:
        keys += ['created_at', 'updated_at']
    order_by = ['id']
    descent = request_data.pop('orderby', None)
    if descent is not None:
        descent = descent.split(',')
        descent = list(set(keys) & set(descent))
        order_by = ['-%s' % i for i in descent]
    return tuple(order_by)
