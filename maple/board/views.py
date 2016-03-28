#*************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: tags.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2016-02-07 12:34:33
#*************************************************************************
#!/usr/bin/env python
# -*- coding=UTF-8 -*-
from flask import render_template, Blueprint,request, g, jsonify
from maple.question.models import Questions, Tags
from maple.board.models import Board_F, Board_S
from maple.question.forms import ReplyForm, PhotoForm, QuestionForm
from maple.main.permissions import que_permission
from maple.main.utils import random_gift
from maple.main.models import RedisData
from maple.forms.forms import return_errors
from flask_login import current_user, login_required
from maple import db
from re import split as sp

site = Blueprint('board', __name__)


@site.url_value_preprocessor
def pull_url(endpoint, values):
    forums_url = values.pop('forums_url')
    g.forums_url = forums_url


@site.url_defaults
def add_url(endpoint, values):
    if 'forums_url' in values or not g.forums_url:
        return
    values['forums_url'] = g.forums_url


@site.route('', defaults={'class_url': None})
@site.route('/<class_url>')
def board(class_url):
    if class_url is None:
        board = Board_F.load_by_name(g.forums_url)
        questions = Questions.load_by_kind(g.forums_url)
        return render_template('board/board.html',
                               board=board,
                               questions=questions,
                               class_url=class_url)
    else:
        board = Board_S.query.join(Board_F).\
            filter(Board_F.enname_f == g.forums_url).\
            filter(Board_S.enname_s == class_url).first_or_404()
        return render_template('board/board_s.html',
                               board=board,
                               class_url=class_url)


@site.route('/<class_url>/view')
def view(class_url):
    qid = request.args.get('qid')
    RedisData.set_read_count(qid)
    form = ReplyForm()
    question = Questions.load_by_id(qid)
    return render_template('question/content.html',
                           question=question,
                           form=form,
                           kind='board')


@site.route('/<class_url>/question', methods=['GET', 'POST'])
@login_required
@que_permission
def question(class_url):
    error = None
    form = QuestionForm()
    fileform = PhotoForm()
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
        question = Questions(title=title, content=content, kind=g.forums_url)
        question.tags = post_tags
        if choice == 'Markdown':
            question.is_markdown = True
        board = Board_S.load_by_name(class_url)
        board.count.topic += 1
        board.count.all_topic += 1
        board.board_f.count.topic += 1
        board.board_f.count.all_topic += 1
        question.board_id = board.id
        question.author_id = current_user.id
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
        board = Board_S.query.join(Board_F).\
            filter(Board_F.enname_f == g.forums_url).\
            filter(Board_S.enname_s == class_url).first_or_404()
        return render_template('question/question.html',
                               fileform=fileform,
                               form=form,
                               board=board)
