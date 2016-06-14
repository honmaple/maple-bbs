#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 13:18:19 (CST)
# Last Update:星期二 2016-6-14 23:20:14 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint, render_template, request
from maple import app
from maple.helpers import is_num
from maple.topic.models import Tags, Topic

site = Blueprint('tag', __name__)


@site.route('', defaults={'tag': None})
@site.route('/<tag>')
def tag(tag):
    if tag is None:
        tags = Tags.query.distinct(Tags.tagname).all()
        data = {'tags': tags}
        return render_template('forums/tag_list.html', **data)
    else:
        page = is_num(request.args.get('page'))
        topics = Topic.query.join(Topic.tags).filter(
            Tags.tagname == tag).paginate(page,
                                          app.config['PER_PAGE'],
                                          error_out=True)
        tag = Tags.query.filter_by(tagname=tag).first_or_404()
        data = {'tag': tag, 'topics': topics}
        return render_template('forums/tag.html', **data)
