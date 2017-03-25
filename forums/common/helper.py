#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: helpers.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 13:56:43 (CST)
# Last Update:星期六 2017-3-25 18:56:12 (CST)
#          By:
# Description:
# **************************************************************************
from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from forums.api.forums.models import Board
from forums.api.topic.forms import TopicForm
from logging.handlers import SMTPHandler
from threading import Thread


def db_session():
    url = current_app.config['SQLALCHEMY_DATABASE_URI']
    engine = create_engine(url)
    session = sessionmaker(bind=engine)
    return session


def form_board():
    form = TopicForm()
    results = []
    for b in Board.query.filter_by(parent_id=None):
        if b.parent is None:
            results.append((b.id, b.name))
        else:
            results.append((b.id, b.name + '   --' + b.parent.name))
    form.category.choices = results
    return form


class ThreadedSMTPHandler(SMTPHandler):
    def emit(self, record):
        thread = Thread(target=SMTPHandler.emit, args=(self, record))
        thread.start()
