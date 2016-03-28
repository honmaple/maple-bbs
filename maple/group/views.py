# *************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: academy.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2016-02-07 12:34:33
# *************************************************************************
# !/usr/bin/env python
# -*- coding=UTF-8 -*-
from flask import (render_template,
                   Blueprint,
                   request,
                   abort,
                   jsonify,
                   redirect,
                   url_for)
from flask_login import (current_user, login_required)
from maple import db
from maple.main.utils import random_gift
from maple.main.models import RedisData
from maple.main.permissions import que_permission
from maple.forms.forms import return_errors, flash_errors
from maple.group.models import Group, Message
from maple.group.forms import ApplyForm
from maple.user.models import User
from maple.question.forms import QuestionForm
from maple.question.models import Questions, Tags
from maple.question.forms import ReplyForm, PhotoForm
from re import split as sp

site = Blueprint('group', __name__)


@site.route('')
def index():
    groups = db.session.query(Group.kind).group_by(Group.kind).all()
    return render_template('group/group.html', groups=groups)


@site.route('/<group>', methods=['GET'])
def group(group):
    group = Group.load_by_name(group)
    form = ApplyForm()
    return render_template('group/view.html', group=group, form=form)


@site.route('/<group>', methods=['POST'])
@login_required
def groups(group):
    group = Group.load_by_name(group)
    form = ApplyForm()
    if form.validate_on_submit():
        content = form.content.data
        letter = Message(send_user=current_user.name,
                         rece_user=group.admin,
                         kind='letter',
                         content=content)
        db.session.add(letter)
        db.session.commit()
        user = User.query.filter_by(name= group.name).first()
        RedisData.set_notice(user)
        return redirect(url_for('group.group', group=group.name))
    else:
        if form.errors:
            flash_errors(form)
            return redirect(url_for('group.group', group=group.name))
        else:
            pass
        abort(404)

@site.route('/<group>/view')
def view(group):
    qid = request.args.get('qid')
    RedisData.set_read_count(qid)
    form = ReplyForm()
    question = Questions.load_by_id(qid)
    return render_template('question/content.html',
                           question=question,
                           form=form,
                           kind='group')


@site.route('/<group>/question', methods=['GET', 'POST'])
@login_required
@que_permission
def question(group):
    group = Group.load_by_name(group)
    form = QuestionForm()
    fileform = PhotoForm()
    error = None
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        choice = form.choice.data
        tags = form.tags.data
        tags = sp(',|;|，|；| ', tags)
        tags = list(set(tags))[:4]
        post_tags = []
        for tag in tags:
            if tag != '':
                t = Tags(author=current_user.name, name=tag)
                post_tags.append(t)
        question = Questions(title=title, content=content, kind=group.kind)
        question.tags = post_tags
        if choice == 'Markdown':
            question.is_markdown = True
        question.is_group = True
        question.group_id = group.id
        question.author_id = current_user.id
        group.count.topic += 1
        group.count.all_topic += 1
        current_user.infor.score -= 5
        '''随机赠送'''
        random_gift()
        db.session.add(question)
        db.session.commit()
        '''使用redis记录'''
        RedisData.set_question()
        RedisData.set_user()
        return jsonify(judge=True, error=error)
    else:
        if form.errors:
            return return_errors(form)
        else:
            pass
        return render_template('group/question.html',
                               group=group,
                               form=form,
                               fileform=fileform)
