#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: upgrade.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-03-29 23:28:43 (CST)
# Last Update:星期四 2017-3-30 14:42:34 (CST)
#          By:
# Description:
# **************************************************************************
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine1 = create_engine('postgresql://postgres:password@localhost/forums1')
session1 = sessionmaker(bind=engine1)()

engine2 = create_engine('postgresql://postgres:password@localhost/forums')
session2 = sessionmaker(bind=engine2)()


def upgrade_board():
    _boards = session1.execute('select * from boards;')
    for i in _boards:
        print(i)
        board = session2.execute(
            "insert into boards (id,name,description) values (:1,:2,:3) RETURNING *",
            {
                '1': i.id,
                '2': i.board,
                '3': i.description
            })
    session2.commit()
    _parent_boards = session1.execute(
        'select parent_board from boards group by parent_board;')
    n = 9
    for i in _parent_boards:
        p = session2.execute(
            "insert into boards (id,name,description) values (:1,:2,:3) RETURNING *",
            {
                '1': n,
                '2': i.parent_board,
                '3': i.parent_board
            })
        session2.commit()
        p = p.fetchone()
        _boards = session1.execute(
            "select * from boards where parent_board = :parent_board", {
                "parent_board": p.name
            })
        for j in _boards:
            q = session2.execute(
                "update boards set parent_id = :1 where id = :2", {
                    '1': p.id,
                    '2': j.id
                })
            session2.commit()
        n += 1


def upgrade_reply():
    _replies = session1.execute('select * from replies')
    for i in _replies:
        print(i)
        reply = session2.execute(
            'insert into replies (id,content,created_at,updated_at,author_id,topic_id) values (:1,:2,:3,:4,:5,:6)',
            {
                '1': i.id,
                '2': i.content,
                '3': i.publish,
                '4': i.publish,
                '5': i.author_id,
                '6': i.topic_id
            })
    session2.commit()


def upgrade_topic():
    _topics = session1.execute('select * from topics')
    for t in _topics:
        print(t)
        content_type = '1' if t.is_markdown else '0'
        topic = session2.execute(
            "insert into topics (id,title,content,content_type,created_at,updated_at,\
            is_good,is_top,author_id,board_id) values (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10) RETURNING *",
            {
                '1': t.id,
                '2': t.title,
                '3': t.content,
                '4': content_type,
                '5': t.publish,
                '6': t.updated,
                '7': t.is_good,
                '8': t.is_top,
                '9': t.author_id,
                '10': t.board_id
            })
    session2.commit()


def upgrade_user():
    results = session1.execute('select * from users;')
    for i in results:
        print(i)
        p = session2.execute(
            "insert into users (id,username,password,email,is_confirmed,\
            is_superuser,register_time) values (:1,:2,:3,:4,:5,:6,:7) RETURNING *",
            {
                '1': i.id,
                '2': i.username,
                '3': i.password,
                '4': i.email,
                '5': i.is_confirmed,
                '6': i.is_superuser,
                '7': i.register_time
            })
        session2.commit()
        p = p.fetchone()
        _info = session1.execute('select * from userinfor where id = :id', {
            'id': i.infor_id
        })
        _info = _info.fetchone()
        info = session2.execute(
            "insert into userinfo (id,avatar,school,word,introduce,user_id) values (:1,:2,:3,:4,:5,:6) RETURNING *",
            {
                '1': _info.id,
                '2': _info.avatar or '',
                '3': _info.school or '',
                '4': _info.word or '',
                '5': _info.introduce or '',
                '6': p.id
            })
        session2.commit()
        _setting = session1.execute('select * from usersetting where id = :id',
                                    {
                                        'id': i.setting_id
                                    })
        _setting = _setting.fetchone()
        setting = session2.execute(
            "insert into usersetting (id,online_status,topic_list,rep_list,\
             ntb_list,collect_list,locale,timezone,user_id) values (:1,:2,:3,:4,:5,:6,:7,:8,:9) RETURNING *",
            {
                '1': _setting.id,
                '2': _setting.online_status,
                '3': _setting.topic_list,
                '4': _setting.rep_list,
                '5': _setting.ntb_list,
                '6': _setting.collect_list,
                '7': _setting.locale,
                '8': _setting.timezone,
                '9': p.id
            })
        session2.commit()


def upgrade_tags():
    _tags = session1.execute('select * from tags;')
    for i in _tags:
        p = session2.execute(
            "insert into tags (id,name,description) values (:1,:2,:3) RETURNING *",
            {
                '1': i.id,
                '2': i.tagname,
                '3': i.summary or i.tagname
            })
    session2.commit()
    _tag_parents = session1.execute('select * from tags_parents;')
    for i in _tag_parents:
        session2.execute('update tags set parent_id = :1 where id = :2', {
            '1': i.parent_id,
            '2': i.tag_id
        })
    session2.commit()
    _tag_topics = session1.execute('select * from tag_topic;')
    for i in _tag_topics:
        p = session2.execute(
            "insert into tag_topic (tag_id,topic_id) values (:1,:2) RETURNING *",
            {
                '1': i.tags_id,
                '2': i.topics_id,
            })
    session2.commit()


def upgrade_collect():
    _collects = session1.execute('select * from collects;')
    for i in _collects:
        print(i)
        p = session2.execute(
            "insert into collects (id,name,description,is_hidden,author_id,created_at,updated_at) values (:1,:2,:3,:4,:5,:6,:7) RETURNING *",
            {
                '1': i.id,
                '2': i.name,
                '3': i.description,
                '4': i.is_privacy,
                '5': i.author_id,
                '6': datetime.now(),
                '7': datetime.now()
            })
    session2.commit()
    _collect_topics = session1.execute('select * from collect_topic;')
    for i in _collect_topics:
        p = session2.execute(
            "insert into topic_collect (collect_id,topic_id) values (:1,:2) RETURNING *",
            {
                '1': i.collect_id,
                '2': i.topic_id
            })
    session2.commit()


def upgrade_like():
    _likes = session1.execute('select * from likes;')
    for i in _likes:
        p = session2.execute(
            "insert into reply_liker (reply_id,liker_id) values (:1,:2) RETURNING *",
            {
                '1': i.reply_id,
                '2': i.author_id
            })
    session2.commit()


def upgrade_follow():
    _followers = session1.execute('select * from follows;')
    for i in _followers:
        print(i)
        if i.following_user_id:
            p = session2.execute(
                "insert into user_follower (follower_id,user_id) values (:1,:2) RETURNING *",
                {
                    '1': i.follower_id,
                    '2': i.following_user_id
                })
        elif i.following_tag_id:
            p = session2.execute(
                "insert into tag_follower (follower_id,tag_id) values (:1,:2) RETURNING *",
                {
                    '1': i.follower_id,
                    '2': i.following_tag_id
                })
        elif i.followinf_topic_id:
            p = session2.execute(
                "insert into topic_follower (follower_id,topic_id) values (:1,:2) RETURNING *",
                {
                    '1': i.follower_id,
                    '2': i.followinf_topic_id
                })
        elif i.following_collect_id:
            p = session2.execute(
                "insert into collect_follower (follower_id,collect_id) values (:1,:2) RETURNING *",
                {
                    '1': i.follower_id,
                    '2': i.following_collect_id
                })
    session2.commit()


def upgrade_setval():
    '''
    psql (9.6.1)
    输入 "help" 来获取帮助信息.

    forums=# \d
                        关联列表
    架构模式 |        名称        |  类型  |  拥有者
    ----------+--------------------+--------+----------
    public   | boards             | 数据表 | postgres
    public   | boards_id_seq      | 序列数 | postgres
    public   | collect_follower   | 数据表 | postgres
    public   | collects           | 数据表 | postgres
    public   | collects_id_seq    | 序列数 | postgres
    public   | replies            | 数据表 | postgres
    public   | replies_id_seq     | 序列数 | postgres
    public   | reply_liker        | 数据表 | postgres
    public   | tag_follower       | 数据表 | postgres
    public   | tag_topic          | 数据表 | postgres
    public   | tags               | 数据表 | postgres
    public   | tags_id_seq        | 序列数 | postgres
    public   | topic_collect      | 数据表 | postgres
    public   | topic_follower     | 数据表 | postgres
    public   | topics             | 数据表 | postgres
    public   | topics_id_seq      | 序列数 | postgres
    public   | user_follower      | 数据表 | postgres
    public   | userinfo           | 数据表 | postgres
    public   | userinfo_id_seq    | 序列数 | postgres
    public   | users              | 数据表 | postgres
    public   | users_id_seq       | 序列数 | postgres
    public   | usersetting        | 数据表 | postgres
    public   | usersetting_id_seq | 序列数 | postgres
    (23 行记录)

    forums=#
    '''
    session2.execute(
        "select setval('boards_id_seq',(select max(id) from boards))")
    session2.execute(
        "select setval('collects_id_seq',(select max(id) from collects))")
    session2.execute("select setval('tags_id_seq',(select max(id) from tags))")
    session2.execute(
        "select setval('topics_id_seq',(select max(id) from topics))")
    session2.execute(
        "select setval('replies_id_seq',(select max(id) from replies))")
    session2.execute(
        "select setval('users_id_seq',(select max(id) from users))")
    session2.execute(
        "select setval('userinfo_id_seq',(select max(id) from userinfo))")
    session2.execute(
        "select setval('usersetting_id_seq',(select max(id) from usersetting))")


if __name__ == '__main__':
    upgrade_board()
    upgrade_user()
    upgrade_topic()
    upgrade_collect()
    upgrade_tags()
    upgrade_reply()
    upgrade_like()
    upgrade_follow()
    upgrade_setval()
