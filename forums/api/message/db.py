#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: db.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-04-01 18:33:37 (CST)
# Last Update: Tuesday 2019-05-07 01:19:46 (CST)
#          By:
# Description:
# **************************************************************************
from flask import url_for
from flask_login import current_user
from forums.extension import db
from forums.jinja import markdown
from forums.common.models import CommonTimeMixin


class MessageText(CommonTimeMixin, db.Model):
    __tablename__ = 'message_text'

    MESSAGE_TYPE_PUBLIC = '0'
    MESSAGE_TYPE_TOPIC = '1'
    MESSAGE_TYPE_REPLY = '2'
    MESSAGE_TYPE_PRIVATE = '3'

    MESSAGE_TYPE = (('0', '系统消息'), ('1', '主题相关'), ('2', '回复相关'), ('3', '私信'))

    STATUS_SUBMIT = '0'
    STATUS_PUBLISH = '1'
    STATUS_UNDO = '2'

    STATUS = (('0', '未发布'), ('1', '已发布'), ('2', '撤销发布'))

    READ_STATUS_UNREAD = '0'
    READ_STATUS_READ = '1'
    READ_STATUS = (('0', '未读'), ('1', '已读'))

    title = db.Column(db.String(128), nullable=False, doc='站内信标题')
    content = db.Column(db.String(1024), nullable=False, doc='站内信内容')
    status = db.Column(
        db.String(128), nullable=False, default=STATUS_SUBMIT, doc='站内信状态')
    message_type = db.Column(
        db.String(128),
        nullable=False,
        default=MESSAGE_TYPE_PUBLIC,
        doc='站内信类型')
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sender = db.relationship(
        'User',
        backref=db.backref('send_messages', lazy='dynamic'),
        lazy='joined',
        uselist=False)

    @classmethod
    def get_choice_dict(cls):
        return dict(
            messagetext=dict(
                status=dict(cls.STATUS),
                message_type=dict(cls.MESSAGE_TYPE),
                read_status=dict(cls.READ_STATUS)))

    def __str__(self):
        return self.title

    def __repr__(self):
        return "<MessageText %r>" % self.title

    @property
    def read_status(self):
        '''
        判断站内信是否已读
        '''
        message = Message.query.filter_by(message_text_id=self.id).first()
        if message:
            return '已读' if message.status == Message.STATUS_READ else '已删除'
        return '未读'


class Message(CommonTimeMixin, db.Model):
    __tablename__ = 'message'

    STATUS_UNREAD = '0'
    STATUS_READ = '1'
    STATUS_DELETE = '2'

    STATUS = (('0', '未读'), ('1', '已读'), ('2', '删除'))

    status = db.Column(
        db.String(128), nullable=False, default=STATUS_UNREAD, doc='站内信状态')
    message_text_id = db.Column(db.Integer, db.ForeignKey('message_text.id'))
    message_text = db.relationship(
        MessageText,
        backref=db.backref("messages", cascade='all,delete', lazy='dynamic'),
        uselist=False,
        lazy='joined')
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver = db.relationship(
        'User',
        backref=db.backref('receive_messages', lazy='dynamic'),
        lazy='joined',
        uselist=False)

    def __str__(self):
        return self.status

    def __repr__(self):
        return "<Message %r>" % self.status

    @property
    def title(self):
        return markdown(self.message_text.title)
        # return self.message_text.title

    @property
    def content(self):
        return self.message_text.content

    @classmethod
    def get_choice_dict(cls):
        return dict(message=dict(status=dict(cls.STATUS)))


class MessageClient(object):
    def system():
        '''
        系统消息
        '''

    @classmethod
    def topic(cls, reply, sender=None):
        '''
        回复主题
        '''
        if sender is None:
            sender = current_user
        topic = reply.topic
        receiver = topic.author
        if sender.id == receiver.id:
            return
        title = '[{}]({})回复了你创建的主题:[{}]({})'.format(
            sender.username, url_for('user.user', username=sender.username),
            topic.title, url_for('topic.topic', topicId=topic.id))
        content = reply.content
        message_text = MessageText(
            sender_id=sender.id, title=title, content=content)
        message_text.save()
        message = Message(receiver=receiver, message_text=message_text)
        message.save()
        receiver.message_count = 1

    @classmethod
    def collect(cls, topic, sender=None):
        '''
        收藏
        '''
        if sender is None:
            sender = current_user
        receiver = topic.author
        if sender.id == receiver.id:
            return
        title = '[{}]({})收藏了你创建的主题:[{}]({})'.format(
            sender.username, url_for('user.user', username=sender.username),
            topic.title, url_for('topic.topic', topicId=topic.id))
        content = 'a'
        message_text = MessageText(
            sender_id=sender.id, title=title, content=content)
        message_text.save()
        message = Message(receiver=receiver, message_text=message_text)
        message.save()
        receiver.message_count = 1

    @classmethod
    def follow(cls, following, sender=None):
        '''
        关注用户,关注主题,关注收藏
        '''
        if sender is None:
            sender = current_user
        if following.__class__.__name__ == 'Topic':
            receiver = following.author
            title = '[{}]({})关注了你创建的主题:[{}]({})'.format(
                sender.username, url_for(
                    'user.user', username=sender.username), following.title,
                url_for('topic.topic', topicId=following.id))
        elif following.__class__.__name__ == 'Collect':
            receiver = following.author
            title = '[{}]({})关注了你创建的收藏:[{}]({})'.format(
                sender.username, url_for(
                    'user.user', username=sender.username), following.title,
                url_for('collect.collect', pk=following.id))
        elif following.__class__.__name__ == 'User':
            receiver = following
            title = '[{}]({})关注了你'.format(
                sender.username, url_for(
                    'user.user', username=sender.username))
        if sender.id == receiver.id:
            return
        content = 'a'
        message_text = MessageText(
            sender_id=sender.id, title=title, content=content)
        message_text.save()
        message = Message(receiver=receiver, message_text=message_text)
        message.save()
        receiver.message_count = 1

    @classmethod
    def reply(cls, reply, sender=None):
        '''
        子回复
        '''
        if sender is None:
            sender = current_user
        receiver = reply.author
        if sender.id == receiver.id:
            return
        topic = reply.topic
        title = '[{}]({})在[{}]({})回复了你'.format(
            sender.username, url_for('user.user', username=sender.username),
            topic.title, url_for('topic.topic', topicId=topic.id))
        content = reply.content
        message_text = MessageText(
            sender_id=sender.id, title=title, content=content)
        message_text.save()
        message = Message(receiver=receiver, message_text=message_text)
        message.save()
        receiver.message_count = 1

    @classmethod
    def like(cls, reply, sender=None):
        '''
        点赞
        '''
        if sender is None:
            sender = current_user
        receiver = reply.author
        if sender.id == receiver.id:
            return
        topic = reply.topic
        title = '[{}]({})在[{}]({})赞了你的回复'.format(
            sender.username, url_for('user.user', username=sender.username),
            topic.title, url_for('topic.topic', topicId=topic.id))
        content = reply.content
        message_text = MessageText(
            sender_id=sender.id, title=title, content=content)
        message_text.save()
        message = Message(receiver=receiver, message_text=message_text)
        message.save()
        receiver.message_count = 1

    def private(cls, message, sender=None):
        '''
        私信
        '''
