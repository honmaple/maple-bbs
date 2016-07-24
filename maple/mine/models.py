#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: models.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 13:32:12 (CST)
# Last Update:星期日 2016-7-24 15:13:39 (CST)
#          By:
# Description:
# **************************************************************************
from maple import db
from maple.tag.models import Tags
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import (generate_password_hash, check_password_hash)
from sqlalchemy import event


class Follow(db.Model):
    __tablename__ = 'follows'
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    following_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    following_tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))
    following_collect_id = db.Column(db.Integer, db.ForeignKey('collects.id'))
    followinf_topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
