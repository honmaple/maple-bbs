#!/usr/bin/env python
# -*- coding=UTF-8 -*-
#*************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: utlis.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2016-02-24 09:28:36
#*************************************************************************
from random import randint
from flask import abort,redirect,url_for
from flask_login import current_user


def random_password():
    from random import sample
    from string import ascii_letters, digits
    password = ''.join(sample(ascii_letters + digits, 8))
    return password

def random_gift():
    if randint(0,100) == 49:
        current_user.score += randint(0,10)
    else:
        pass

def load_pages(pages,pid):
    if not pages:
        pages = 1
    else:
        if int(pages)%12 == 0:
            pages = int(pages)//12
        else:
            pages = int(pages)//12 + 1
    if pid < 1:
        abort(404)
    if pages != 0 and pid > pages:
        abort(404)
    return pages

def load_pid(pid):
    if pid is None:
        pid = 1
    else:
        if pid.isdigit():
            pid = int(pid)
        else:
            abort(404)
    return pid

def load_qid(qid):
    if qid is None:
        return redirect(url_for('tags.index'))
    else:
        if qid.isdigit():
            qid = int(qid)
        else:
            abort(404)
    return qid

