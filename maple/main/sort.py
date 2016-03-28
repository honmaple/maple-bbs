# *************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: sort.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2016-02-14 21:32:42
# *************************************************************************
# !/usr/bin/env python
# -*- coding=UTF-8 -*-
from flask import request
from maple.question.models import Questions,Tags
from maple.group.models import Group
from maple.board.models import Board_F, Board_S
from datetime import datetime, timedelta


def form_judge(form):
    '''
    0: all topic
    1: one day
    2: one week
    3: one month

    0: time
    1: author

    0: desc
    1: asc
    '''
    t1 = form.display.data
    t2 = form.sort.data
    t3 = form.st.data
    data = form_sort(t1, t2, t3)
    return data


def form_sort(t1, t2, t3):
    url = request.args.get('by')
    uid = request.args.get('uid')

    if t1 == 0:
        time = datetime.now() - timedelta(days=365)
    elif t1 == 1:
        time = datetime.now() - timedelta(days=1)
    elif t1 == 2:
        time = datetime.now() - timedelta(days=7)
    else:
        time = datetime.now() - timedelta(days=30)

    # 发表时间
    if t2 == 0:
        if t3 == 0:
            if url == 'board_f':
                data = Board_F.load_by_id(uid)
                data = Questions.query.filter(
                    Questions.time > time, Questions.kind ==
                    data.enname_f).order_by(Questions.time.desc()).all()
            elif url == 'board_s':
                data = Board_S.load_by_id(uid)
                data = Questions.query.filter(
                    Questions.time > time, Questions.board_id ==
                    data.id).order_by(Questions.time.desc()).all()
            elif url == 'tags':
                data = Questions.query.join(Questions.tags).filter(
                    Questions.time > time, Tags.name==
                    uid).order_by(Questions.time.desc()).all()
            elif url == 'group':
                data = Group.load_by_id(uid)
                data = Questions.query.filter(
                    Questions.time > time, Questions.group_id ==
                    data.id).order_by(Questions.time.desc()).all()
            else:
                data = None
            return data
        else:
            if url == 'board_f':
                data = Board_F.load_by_id(uid)
                data = Questions.query.filter(
                    Questions.time > time, Questions.kind ==
                    data.enname_f).order_by(Questions.time).all()
            elif url == 'board_s':
                data = Board_S.load_by_id(uid)
                data = Questions.query.filter(
                    Questions.time > time, Questions.board_id ==
                    data.id).order_by(Questions.time).all()
            elif url == 'tags':
                data = Questions.query.join(Questions.tags).filter(
                    Questions.time > time, Tags.name==
                    uid).order_by(Questions.time).all()
            elif url == 'group':
                data = Group.load_by_id(uid)
                data = Questions.query.filter(
                    Questions.time > time, Questions.group_id ==
                    data.id).order_by(Questions.time).all()
            else:
                data = None
            return data
    # 作者
    else:
        if t3 == 0:
            if url == 'board_f':
                data = Board_F.load_by_id(uid)
                data = Questions.query.filter(
                    Questions.time > time, Questions.kind ==
                    data.enname_f).order_by(Questions.author_id.desc()).all()
            elif url == 'board_s':
                data = Board_S.load_by_id(uid)
                data = Questions.query.filter(
                    Questions.time > time, Questions.board_id ==
                    data.id).order_by(Questions.author_id.desc()).all()
            elif url == 'tags':
                data = Questions.query.join(Questions.tags).filter(
                    Questions.time > time, Tags.name==
                    uid).order_by(Questions.author_id.desc()).all()
            elif url == 'group':
                data = Group.load_by_id(uid)
                data = Questions.query.filter(
                    Questions.time > time, Questions.group_id ==
                    data.id).order_by(Questions.author_id.desc()).all()
            else:
                data = None
            return data
        else:
            if url == 'board_f':
                data = Board_F.load_by_id(uid)
                data = Questions.query.filter(
                    Questions.time > time, Questions.kind ==
                    data.enname_f).order_by(Questions.author_id).all()
            elif url == 'board_s':
                data = Board_S.load_by_id(uid)
                data = Questions.query.filter(
                    Questions.time > time, Questions.board_id ==
                    data.id).order_by(Questions.author_id).all()
            elif url == 'tags':
                data = Questions.query.join(Questions.tags).filter(
                    Questions.time > time, Tags.name==
                    uid).order_by(Questions.author_id).all()
            elif url == 'group':
                data = Group.load_by_id(uid)
                data = Questions.query.filter(
                    Questions.time > time, Questions.group_id ==
                    data.id).order_by(Questions.author_id).all()
            else:
                data = None
            return data
