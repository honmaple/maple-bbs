#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: controls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-06-15 10:22:42 (CST)
# Last Update:星期日 2016-8-7 17:41:8 (CST)
#          By:
# Description:
# **************************************************************************
from flask import current_app
from flask_login import current_user
from sqlalchemy.sql import func
from maple import db
from maple.helpers import make_uid
from maple.main.models import RedisData
from maple.forums.controls import reply as notice_reply
from maple.forums.controls import rereply as notice_rereply
from maple.tag.models import Tags
from maple.user.models import User
from .models import Topic, Reply, Like
# from .redis import get_detail_cache
from re import split as sp
from re import findall
from maple.helpers import html_clean


def vote(count):
    if count > 0:
        html = '''
                <a id="topic-up-vote" class="vote" href="javascript:void(0)" style="text-decoration:none;">
                    <i class="icon-chevron-up">%d</i>
                </a>
                <a id="topic-down-vote" class="vote" href="javascript:void(0)" style="text-decoration:none;">
                    <i class="icon-chevron-down"></i>
                </a>
        ''' % (count)
    elif count == 0:
        html = '''
                <a id="topic-up-vote" class="vote" href="javascript:void(0)" style="text-decoration:none;">
                    <i class="icon-chevron-up"></i>
                </a>
                <a  id="topic-down-vote" class="vote" href="javascript:void(0)" style="text-decoration:none;">
                    <i class="icon-chevron-down"></i>
                </a>
        '''

    else:
        html = '''
                <a id="topic-up-vote" class="vote" href="javascript:void(0)" style="text-decoration:none;">
                    <i class="icon-chevron-up"></i>
                </a>
                <a  id="topic-down-vote" class="vote" href="javascript:void(0)" style="text-decoration:none;">
                    <i class="icon-chevron-down">%d</i>
                </a>
        ''' % (count)
    return html


class TopicModel(object):
    def get_list(page):
        topics = Topic.query.filter_by(is_top=False).paginate(
            page, current_app.config['PER_PAGE'],
            error_out=True)
        top_topics = Topic.query.filter_by(is_top=True).limit(5).all()
        return topics, top_topics

    def get_detail(page, topicId, order='time'):
        topic = Topic.query.filter_by(uid=topicId).first_or_404()
        if order == 'like':
            replies = Reply.query.outerjoin(Like).filter(
                Reply.topic_id == topic.id).group_by(Reply.id).order_by(
                    func.count(Like.id).desc()).paginate(
                        page, current_app.config['PER_PAGE'], True)
        else:
            replies = Reply.query.filter_by(
                topic_id=topic.id).order_by(Reply.publish.asc()).paginate(
                    page, current_app.config['PER_PAGE'], True)
        RedisData.set_read_count(topic.id)
        return topic, replies

    def post(form):
        topic = Topic()
        topic.title = form.title.data
        topic.content = html_clean(form.content.data)
        topic.is_markdown = True if form.choice.data == 1 else False
        topic.uid = make_uid()
        topic.author = current_user
        tags = sp(',|;|，|；| ', form.tags.data)
        tags = [x for x in list(set(tags)) if x != ''][:4]
        post_tags = []
        for tag in tags:
            if tag != '':
                exsit_tag = Tags.query.filter_by(tagname=tag).first()
                if exsit_tag is not None:
                    post_tags.append(exsit_tag)
                    if exsit_tag not in current_user.following_tags:
                        current_user.following_tags.append(exsit_tag)
                else:
                    t = Tags()
                    t.tagname = tag
                    post_tags.append(t)
                    current_user.following_tags.append(t)
        topic.tags = post_tags
        topic.board_id = form.category.data
        db.session.add(topic)
        db.session.commit()
        current_user.following_topics.append(topic)
        topic.board.count.topics += 1
        topic.board.count.all_topics += 1
        db.session.commit()
        RedisData.set_topics()
        return topic

    def put(form, topicId):
        topic = Topic.query.filter_by(uid=topicId).first_or_404()
        topic.title = form.title.data
        topic.content = html_clean(form.content.data)
        topic.is_markdown = True if form.choice.data == 1 else False
        tags = sp(',|;|，|；| ', form.tags.data)
        tags = [x for x in list(set(tags)) if x != ''][:4]
        post_tags = []
        for tag in tags:
            if tag != '':
                exsit_tag = Tags.query.filter_by(tagname=tag).first()
                if exsit_tag is not None:
                    post_tags.append(exsit_tag)
                    if exsit_tag not in current_user.following_tags:
                        current_user.following_tags.append(exsit_tag)
                else:
                    t = Tags()
                    t.tagname = tag
                    post_tags.append(t)
                    current_user.following_tags.append(t)
        topic.tags = post_tags
        topic.board_id = form.category.data
        db.session.commit()
        return topic


class ReplyModel(object):
    def post(self, form, uid):
        reply = Reply()
        content = html_clean(form.content.data)
        content, usernames = self.at_user(content)
        reply.content = content
        reply.author = current_user
        reply.topic_id = uid
        db.session.add(reply)
        db.session.commit()
        topic = reply.topic
        self.reply_count(topic, reply)
        self.reply_notice(topic, reply, usernames)
        return reply

    def at_user(self, content):
        usernames = findall(r'@([\u4e00-\u9fa5\w\-]+)', content)
        ex_usernames = []
        for username in usernames:
            user = User.query.filter_by(username=username).first()
            if user is not None and username != current_user.username:
                ex_usernames.append(user.username)
                href = '/u/' + username
                u = '@' + username + ' '
                content = content.replace(u, '@<a href="%s">%s</a> ' %
                                          (href, username))
        usernames = list(set(ex_usernames))
        return content, usernames

    def reply_count(self, topic, reply):
        topic.board.count.all_topics += 1
        RedisData.set_replies(topic.id)

    def reply_notice(self, topic, reply, usernames):
        author = topic.author
        usernames = [username
                     for username in usernames
                     if (username != current_user.username)]
        if author.id != current_user.id:
            if author.username in usernames:
                notice_rereply(topic, reply, author.username)
            else:
                notice_reply(topic, reply)
                for username in usernames:
                    notice_rereply(topic, reply, username)
