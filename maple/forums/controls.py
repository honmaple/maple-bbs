#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: controls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-06-30 19:39:13 (CST)
# Last Update:星期日 2016-8-7 16:51:10 (CST)
#          By:
# Description:
# **************************************************************************
from flask import url_for
from flask_login import current_user
from maple.helpers import replies_page
from maple.user.models import User
from .models import db
from .models import Notice


def rereply(topic, reply, rece_username):
    user = User.query.filter_by(username=rece_username).first()
    page = replies_page(topic.id)
    url = url_for('topic.topic',
                  topicId=topic.uid,
                  page=page,
                  _anchor='reply' + str(reply.id))
    notice = Notice()
    notice.category = 'rereply'
    notice.content = {'url': url,
                      'content': reply.content[:100],
                      'title': topic.title}
    notice.rece_id = user.id
    notice.send_user = current_user
    db.session.add(notice)
    db.session.commit()


def reply(topic, reply):
    page = replies_page(topic.id)
    url = url_for('topic.topic',
                  topicId=topic.uid,
                  page=page,
                  _anchor='reply' + str(reply.id))
    notice = Notice()
    notice.category = 'reply'
    notice.content = {'url': url,
                      'content': reply.content[:100],
                      'title': topic.title}
    notice.rece_id = topic.author_id
    notice.send_user = current_user
    db.session.add(notice)
    db.session.commit()


def collect(topic):
    url = url_for('topic.topic', topicId=topic.uid)
    notice = Notice()
    notice.category = 'collect'
    notice.content = {'url': url, 'title': topic.title}
    notice.rece_id = topic.author_id
    notice.send_user = current_user
    db.session.add(notice)
    db.session.commit()


def like(reply):
    topic = reply.topic
    url = url_for('topic.topic',
                  topicId=topic.uid,
                  _anchor='reply-' + str(reply.id))
    notice = Notice()
    notice.category = 'like'
    notice.content = {'url': url,
                      'title': topic.title,
                      'content': reply.content[:100]}
    notice.rece_id = reply.author_id
    notice.send_user = current_user
    db.session.add(notice)
    db.session.commit()


def user(userId):
    notice = Notice()
    notice.category = 'user'
    notice.rece_id = userId
    notice.send_user = current_user
    db.session.add(notice)
    db.session.commit()
