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
from flask import Blueprint, render_template, g, request, abort
from flask_login import current_user,login_required
from maple import app, db
from maple.helpers import is_num
from maple.user.models import User
from maple.forums.models import Notice, Board
from maple.topic.models import Tags, Topic

site = Blueprint('forums', __name__)


@site.route('/', methods=['GET'])
def index():
    topics = Topic.query.filter_by(is_good=True).paginate(1, 10)
    if not topics.items:
        topics = Topic.query.paginate(1, 10)
    data = {'topics': topics}
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


@site.route('/notices', defaults={'page': 1})
@site.route('/notices/?page=<int:page>')
@login_required
def notice(page):
    notices = Notice.query.join(Notice.rece_user).filter(
        User.username == current_user.username).paginate(
            page, app.config['PER_PAGE'],
            error_out=True)
    return render_template('forums/notice.html', notices=notices)


@site.route('/userlist')
@login_required
def userlist():
    page = is_num(request.args.get('page'))
    users = User.query.paginate(page, app.config['PER_PAGE'], error_out=True)
    data = {'users': users}
    return render_template('forums/userlist.html', **data)


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
