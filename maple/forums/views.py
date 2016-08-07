#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 13:18:19 (CST)
# Last Update:星期二 2016-8-2 20:21:17 (CST)
#          By:
# Description:
# **************************************************************************
from flask import (render_template, g, request, abort, redirect, flash,
                   url_for, current_app)
from flask_login import current_user
from flask_babelex import gettext as _
from flask_maple.forms import flash_errors
from maple.helpers import is_num
from maple.user.models import User
from maple.forums.models import Notice, Board
from maple.topic.models import Topic
from .forms import MessageForm
from maple import cache, db


def index():
    topics = Topic.query.filter_by(is_good=True, is_top=False).paginate(1, 10)
    top_topics = Topic.query.filter_by(is_top=True).limit(5)
    if not topics.items:
        topics = Topic.query.filter_by(is_top=False).paginate(1, 10)
    data = {'title': '', 'topics': topics, 'top_topics': top_topics}
    return render_template('forums/index.html', **data)


def forums():
    boards = {}
    parent_boards = db.session.query(Board.parent_board).group_by(
        Board.parent_board)
    for parent_board in parent_boards:
        child_board = Board.query.filter_by(parent_board=parent_board).all()
        boards[parent_board[0]] = child_board
    data = {'title': _('Index - '), 'boards': boards}
    return render_template('forums/forums.html', **data)


@cache.cached(timeout=60)
def notice():
    page = is_num(request.args.get('page'))
    notices = Notice.query.filter_by(
        rece_id=current_user.id).order_by(Notice.publish.desc()).paginate(
            page, current_app.config['PER_PAGE'],
            error_out=True)
    unread_notices = Notice.query.filter_by(rece_id=current_user.id,
                                            is_read=False).all()
    if unread_notices:
        for notice in unread_notices:
            notice.is_read = True
        db.session.commit()
    data = {'title': _('Notice - '), 'notices': notices}
    return render_template('forums/notice.html', **data)


def userlist():
    page = is_num(request.args.get('page'))
    users = User.query.paginate(page,
                                current_app.config['PER_PAGE'],
                                error_out=True)
    data = {'title': _('Userlist - '), 'users': users}
    return render_template('forums/userlist.html', **data)


def message(receId):
    form = MessageForm()
    rece_user = User.query.filter_by(id=receId).first_or_404()
    if form.validate_on_submit() and request.method == "POST":
        message = Notice()
        message.category = 'privacy'
        message.content = {'content': form.message.data}
        message.rece_user = rece_user
        message.send_id = current_user.id
        db.session.add(message)
        db.session.commit()
        flash(_('send succeccfully'), category='success')
        return redirect(url_for('user.user', user_url=rece_user.username))
    else:
        if form.errors:
            flash_errors(form)
    return redirect(url_for('user.user', user_url=rece_user.username))


@cache.cached(timeout=60)
def about():
    data = {'title': _('About - ')}
    return render_template('forums/about.html', **data)


@cache.cached(timeout=60)
def help():
    data = {'title': _('Help - ')}
    return render_template('forums/help.html', **data)


@cache.cached(timeout=60)
def contact():
    data = {'title': _('Contact - ')}
    return render_template('forums/contact.html', **data)


def order():
    from maple.main.orderby import form_judge
    form = g.sort_form
    if form.validate_on_submit():
        topics = form_judge(form)
        data = {'topics': topics}
        return render_template('base/sort.html', **data)
    else:
        abort(404)
