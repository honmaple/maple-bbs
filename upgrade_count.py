#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: upgrade_coount.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-04-02 13:00:02 (CST)
# Last Update:星期日 2017-4-2 13:47:2 (CST)
#          By:
# Description:
# **************************************************************************
from runserver import app
from forums.api.topic.models import Topic, Reply
from forums.api.forums.models import Board
from forums.api.user.models import User
from forums.extension import redis_data


def topic():
    topics = Topic.query.all()
    for t in topics:
        print('topic', t.title)
        key = 'count:topic:{}'.format(t.id)
        reply_count = t.replies.count()
        read_key = 'topic:{}'.format(t.id)
        read_count = redis_data.hget(read_key, 'read')
        if reply_count:
            redis_data.hset(key, 'replies', reply_count)
        if read_count:
            redis_data.hset(key, 'read', read_count)
        # 删除旧key
        redis_data.delete(read_key)


def reply():
    replies = Reply.query.all()
    for t in replies:
        print('reply', t.id)
        key = 'count:reply:{}'.format(t.id)
        liker_count = t.likers.count()
        if liker_count:
            redis_data.hset(key, 'liker', liker_count)


def user():
    users = User.query.all()
    for t in users:
        print('user', t.username)
        key = 'count:user:{}'.format(t.id)
        topic_count = t.topics.count()
        reply_count = t.replies.count()
        if topic_count:
            redis_data.hset(key, 'topic', topic_count)
        if reply_count:
            redis_data.hset(key, 'replies', topic_count)
        # 删除旧key
        old_user_key = 'user:{}'.format(t.id)
        redis_data.delete(old_user_key)


def board():
    boards = Board.query.all()
    for b in boards:
        print('board', b.name)
        key = 'count:board:{}'.format(b.id)
        topic_count = Topic.query.filter_by(board_id=b.id).count()
        reply_count = Reply.query.filter_by(topic__board_id=b.id).count()
        post_count = topic_count + reply_count
        if topic_count:
            redis_data.hset(key, 'topic', topic_count)
        if post_count:
            redis_data.hset(key, 'post', topic_count)


def main():
    with app.app_context():
        topic()
        board()
        user()
        reply()


if __name__ == '__main__':
    main()
