#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 13:18:19 (CST)
# Last Update:星期四 2016-6-30 20:32:38 (CST)
#          By:
# Description:
# **************************************************************************
from flask import (Blueprint, render_template, g, request, abort, redirect,
                   flash, url_for)
from flask_login import current_user, login_required
from flask_maple.forms import flash_errors
from maple import app, db
from maple.helpers import is_num
from maple.user.models import User
from maple.forums.models import Notice, Board
from maple.topic.models import Topic
from .forms import MessageForm

site = Blueprint('forums', __name__)


@site.route('/', methods=['GET'])
def index():
    topics = Topic.query.filter_by(is_good=True, is_top=False).paginate(1, 10)
    top_topics = Topic.query.filter_by(is_top=True).limit(5).all()
    if not topics.items:
        topics = Topic.query.paginate(1, 10)
    data = {'topics': topics, 'top_topics': top_topics}
    return render_template('forums/index.html', **data)


@site.route('/index')
def forums():
    boards = {}
    parent_boards = db.session.query(Board.parent_board).group_by(
        Board.parent_board)
    for parent_board in parent_boards:
        child_board = Board.query.filter_by(parent_board=parent_board).all()
        boards[parent_board[0]] = child_board
    data = {'boards': boards}
    return render_template('forums/forums.html', **data)


@site.route('/notices')
@login_required
def notice():
    page = is_num(request.args.get('page'))
    notices = Notice.query.filter_by(
        rece_id=current_user.id).order_by(Notice.publish.desc()).paginate(
            page, app.config['PER_PAGE'],
            error_out=True)
    data = {'notices': notices}
    return render_template('forums/notice.html', **data)


@site.route('/userlist')
@login_required
def userlist():
    page = is_num(request.args.get('page'))
    users = User.query.paginate(page, app.config['PER_PAGE'], error_out=True)
    data = {'users': users}
    return render_template('forums/userlist.html', **data)


@site.route('/messages/<int:receId>', methods=['POST'])
@login_required
def message(receId):
    form = MessageForm()
    rece_user = User.query.filter_by(id=receId).first_or_404()
    if form.validate_on_submit() and request.method == "POST":
        message = Notice()
        message.category = 'privacy'
        message.content = form.message.data
        message.rece_user = rece_user
        message.send_id = current_user.id
        db.session.add(message)
        db.session.commit()
        flash('成功发送', category='success')
        return redirect(url_for('user.user', user_url=rece_user.username))
    else:
        if form.errors:
            flash_errors(form)
    return redirect(url_for('user.user', user_url=rece_user.username))


@site.route('/about')
def about():
    return render_template('forums/about.html')


@site.route('/help')
def help():
    return render_template('forums/help.html')


@site.route('/order', methods=['POST'])
def order():
    from maple.main.orderby import form_judge
    form = g.sort_form
    if form.validate_on_submit():
        topics = form_judge(form)
        data = {'topics': topics}
        return render_template('base/sort.html', **data)
    else:
        abort(404)
