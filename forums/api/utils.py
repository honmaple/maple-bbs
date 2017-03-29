#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: utils.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-03-29 13:33:03 (CST)
# Last Update:星期三 2017-3-29 13:43:40 (CST)
#          By:
# Description:
# **************************************************************************
from datetime import datetime, timedelta

one_day = datetime.now() + timedelta(days=-1)
one_month = datetime.now() + timedelta(days=-30)
one_year = datetime.now() + timedelta(years=-1)


def gen_topic_filter(query_dict=dict(), keys=[], equal_key=[], user=None):
    filter_dict = {}
    keys = list(set(keys) & set(query_dict.keys()))
    for k in keys:
        if k in equal_key:
            filter_dict.update(**{k: query_dict[k]})
        else:
            new_k = '%s__contains' % k
            filter_dict.update(**{new_k: query_dict[k]})
    if user is not None and user.is_authenticated:
        filter_dict.update(user__id=user.id)
    within = query_dict.pop('within', None)
    if within is not None:
        if within == 1:
            filter_dict.update(created_at__gte=one_day)
        elif within == 2:
            filter_dict.update(created_at__gte=one_month)
        elif within == 3:
            filter_dict.update(created_at__gte=one_year)
    return filter_dict


def gen_topic_orderby(query_dict=dict(), keys=[], date_key=True):
    keys.append('id')
    if date_key:
        keys += ['created_at', 'updated_at']
    order_by = ['id']
    descent = query_dict.pop('orderby', None)
    if descent is not None:
        descent = descent.split(',')
        descent = list(set(keys) & set(descent))
        order_by = ['-%s' % i for i in descent]
    return tuple(order_by)
