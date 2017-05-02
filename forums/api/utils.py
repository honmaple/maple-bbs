#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: utils.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-03-29 13:33:03 (CST)
# Last Update:星期二 2017-5-2 12:21:37 (CST)
#          By:
# Description:
# **************************************************************************
from datetime import datetime, timedelta

one_day = datetime.now() + timedelta(days=-1)
one_week = datetime.now() + timedelta(days=-7)
one_month = datetime.now() + timedelta(days=-30)
one_year = datetime.now() + timedelta(days=-365)


def gen_topic_filter(query_dict=dict(), keys=[], equal_key=[], user=None):
    filter_dict = {}
    keys = list(set(keys) & set(query_dict.keys()))
    within = query_dict.pop('within', None)
    if within == '1':
        filter_dict.update(created_at__gte=one_day)
    elif within == '2':
        filter_dict.update(created_at__gte=one_week)
    elif within == '3':
        filter_dict.update(created_at__gte=one_month)
    elif within == '4':
        filter_dict.update(created_at__gte=one_year)
    for k in keys:
        if k in equal_key:
            filter_dict.update(**{k: query_dict[k]})
        else:
            new_k = '%s__contains' % k
            filter_dict.update(**{new_k: query_dict[k]})
    if user is not None and user.is_authenticated:
        filter_dict.update(user__id=user.id)
    return filter_dict


def gen_topic_orderby(query_dict=dict(), keys=[], date_key=True):
    keys.append('id')
    order_by = ['-id']
    # order_by = ['-is_top', '-id']
    orderby = query_dict.pop('orderby', None)
    desc = query_dict.pop('desc', None)
    if orderby == '0':
        order_by = ['created_at']
    elif orderby == '1':
        order_by = ['author_id']
    if desc == '0':
        order_by = ['-%s' % i for i in order_by]
    order_by = ['-is_top'] + order_by
    return tuple(order_by)
