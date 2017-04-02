#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: helpers.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 13:56:43 (CST)
# Last Update:星期六 2017-4-1 23:43:49 (CST)
#          By:
# Description:
# **************************************************************************
from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from logging.handlers import SMTPHandler
from threading import Thread


def db_session():
    url = current_app.config['SQLALCHEMY_DATABASE_URI']
    engine = create_engine(url)
    session = sessionmaker(bind=engine)
    return session


class ThreadedSMTPHandler(SMTPHandler):
    def emit(self, record):
        thread = Thread(target=SMTPHandler.emit, args=(self, record))
        thread.start()
