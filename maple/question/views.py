# *************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: index.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2015-11-25 02:21:04
# *************************************************************************
# !/usr/bin/env python
# -*- coding=UTF-8 -*-
from flask import (Blueprint, request,
                   abort, flash,
                   Markup, jsonify,
                   redirect, url_for,
                   g, render_template)
from flask_login import current_user, login_required
from maple.group.models import Message
from maple.question.models import Collector, Lover, Replies
from maple.question.forms import ReplyForm
from maple.user.models import User
from maple.main.filters import safe_clean
from maple.main.utils import random_gift, load_qid
from maple.main.models import RedisData
from maple.main.permissions import rep_permission
from maple import db
from datetime import datetime

site = Blueprint('question', __name__)


@site.route('/preview', methods=['GET', 'POST'])
@login_required
def preview():
    if request.method == "POST":
        from misaka import Markdown, HtmlRenderer
        choice = request.values.get('choice')
        content = request.values.get('content')
        if choice == 'Default':
            return safe_clean(content)
        else:
            html = HtmlRenderer()
            markdown = Markdown(html)
            return Markup(markdown(content))
    else:
        abort(404)


@site.route('/uploads', methods=('GET', 'POST'))
@login_required
def upload():
    abort(404)
    #  form = PhotoForm()
    #  if form.validate_on_submit():
        #  filedata = form.photo.data
        #  print(filedata)
        #  filename = secure_filename(form.photo.data.filename)
        #  print(filename)
        #  form.photo.data.save(os.path.join(app.static_folder, filename))
        #  return jsonify(judge=True, error=filename)
    #  else:
        #  if form.errors is not None:
            #  return return_errors(form)
        #  else:
            #  return jsonify(judge=False, error='上传失败')


@site.route('/uploads/<filename>')
def send_file(filename):
    abort(404)
    #  return send_from_directory(app.static_folder, filename)


@site.route('/collect', methods=['GET', 'POST'])
@login_required
def collect():
    if request.method == "POST":
        qid = request.values.get('qid')
        collect = Collector.load(qid, current_user.id)
        if collect is not None:
            db.session.delete(collect)
            db.session.commit()
            RedisData.set_collect(current_user, -1)
            return jsonify(judge=True)
        else:
            collect = Collector()
            collect.question_id = qid
            collect.user_id = current_user.id
            db.session.add(collect)
            db.session.commit()
            user = User.load_by_id(collect.user_id)
            if current_user.name != user.name:
                message = Message(send_user=current_user.name,
                                rece_user=user.name,
                                kind='collect',
                                content='a')
                message.question_id = qid
                db.session.add(message)
                db.session.commit()
                RedisData.set_notice(user, 1)
            else:
                pass
            RedisData.set_collect(current_user, 1)
            return jsonify(judge=True)
    else:
        abort(404)


@site.route('/love', methods=['GET', 'POST'])
@login_required
def love():
    '''点赞'''
    if request.method == "POST":
        rid = request.values.get('rid')
        print(rid)
        love = Lover.load(rid, current_user.id)
        if love is not None:
            db.session.delete(love)
            db.session.commit()
            RedisData.set_love(current_user, -1)
            flash('成功取消赞')
            return jsonify(judge=True)
        else:
            love = Lover()
            love.reply_id = rid
            love.user_id = current_user.id
            db.session.add(love)
            db.session.commit()
            user = User.load_by_id(love.user_id)
            if current_user.name != user.name:
                message = Message(send_user=current_user.name,
                                rece_user=user.name,
                                kind='love',
                                content='a')
                message.reply_id = rid
                db.session.add(message)
                db.session.commit()
                RedisData.set_notice(user, 1)
            else:
                pass
            RedisData.set_love(current_user, 1)
            flash('赞成功')
            return jsonify(judge=True)
    else:
        abort(404)


@site.route('/reply', methods=['GET', 'POST'])
@login_required
@rep_permission
def reply():
    error = None
    form = ReplyForm()
    if form.validate_on_submit() and request.method == "POST":
        qid = request.args.get('qid')
        qid = load_qid(qid)
        quote = request.get_json()['quote']
        content = form.content.data
        reply = Replies(content=content, quote=quote)
        reply.question_id = qid
        reply.author_id = current_user.id
        current_user.infor.score -= 1
        '''随机赠送'''
        random_gift()
        db.session.add(reply)
        db.session.commit()
        '''消息通知'''
        if current_user.name != reply.question.author.name:
            message = Message(send_user=current_user.name,
                            rece_user=reply.question.author.name,
                            kind='reply',
                            content=reply.content)
            message.reply_id = reply.id
            RedisData.set_notice(reply.question.author)
            db.session.add(message)
        reply.question.last_author = current_user.name
        reply.question.last_time = datetime.now()
        if reply.question.is_group:
            reply.question.group.count.all_topic += 1
        else:
            reply.question.board.count.all_topic += 1
            reply.question.board.board_f.count.all_topic += 1
        db.session.commit()
        '''使用redis记录'''
        RedisData.set_replies(qid)
        RedisData.set_user_all()
        return jsonify(judge=True, error=error)
    else:
        if form.content.errors:
            error = form.content.errors
            return jsonify(judge=False, error=error)
        else:
            pass
        return redirect(url_for('forums.forums'))


@site.route('/rreply', methods=['GET', 'POST'])
@login_required
def rreply():
    if request.method == "POST":
        rid = request.values.get('rid')
        reply = Replies.load_by_id(rid)
        if reply.quote is None:
            content = '<blockquote>引用了<b>%s</b> 的回复:<br>%s</blockquote>\n' % (
                reply.author.name, reply.content)
        else:
            content = '<blockquote>引用了<b>%s</b> 的回复:' + \
                      '<br>%s%s</blockquote>\n' % (
                reply.author.name, reply.quote, reply.content)
        #  if current_user.name != reply.author:
        #  '''提醒'''
        #  user = User.get_by_name(reply.author)
        #  RedisData.set_notice(user)
        return content
    else:
        abort(404)


@site.route('/order', methods=['GET', 'POST'])
def order():
    from maple.main.sort import form_judge
    form = g.sortform
    if form.validate_on_submit() and request.method == "POST":
        questions = form_judge(form)
        return render_template('base/sort.html', questions=questions)
    else:
        abort(404)
