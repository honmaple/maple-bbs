#*************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: permissions.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2015-12-12 20:28:00
#*************************************************************************
#!/usr/bin/env python
# -*- coding=UTF-8 -*-
from maple import app
from flask_login import current_user
from flask_principal import Permission, RoleNeed, UserNeed, identity_loaded
from flask import abort, jsonify
from functools import wraps
from flask import g, redirect, flash, url_for
from maple import redis_data
from maple.group.models import Group
from time import time
from flask import request
from collections import namedtuple
from functools import partial

Need = namedtuple('need', ['method', 'value'])
EditQuestionNeed = partial(Need, 'id')
PostNeed = partial(Need, 'post')
GroupNeed = partial(Need, 'id')
BoardNeed = partial(Need, 'id')
UserNameNeed = partial(Need, 'name')
ShowNeed = partial(Need, 'permission')

class MyPermission(object):
    def __init__(self,required=None,name=None):
        self.required = required

    def __call__(self, func):
        @wraps(func)
        def decorator(*args, **kwargs):
            if not self.allow():
                return self.action()
            return func(*args, **kwargs)
        return decorator

    def allow(self):
        return False

    def action(self):
        abort(403)

class QuePermission(MyPermission):
    def allow(self):
        if current_user.infor.score > 5:
            return True
        else:
            return False

    def action(self):
        flash('你的积分不足，不能发帖,如有问题请联系管理员')
        return redirect(url_for('user.index',user_url=current_user.name))

class RepPermission(MyPermission):
    def allow(self):
        if current_user.infor.score > 1:
            return True
        else:
            return False

    def action(self):
        error = '你的积分不足，不能回复,如有问题请联系管理员'
        return jsonify(judge=False,error=error)

class OwnPermission(MyPermission):
    def allow(self):
        if current_user.name == g.user_url:
            return True
        else:
            return False

    def action(self):
        return redirect(url_for('user.setting',user_url=current_user.name))

class GuestPermission(MyPermission):
    def allow(self):
        if not g.user.is_authenticated:
            return True
        else:
            return False

    def action(self):
        flash('你已经登陆,不能重复登陆')
        return redirect(url_for('forums.forums'))

class TimePermission(MyPermission):
    def allow(self):
        user = 'user:%s' % str(current_user.id)
        last_time = redis_data.hget(user, 'send_email_time')
        now_time = int(time()) + 28800
        if last_time is None:
            last_time = now_time
            return True
        else:
            last_time = int(last_time)
        if last_time < now_time - 3600:
            return True
        else:
            return False

    def action(self):
        error = u'你的验证链接还未过期，请尽快验证'
        return error

que_permission = QuePermission()
rep_permission = RepPermission()
own_permission = OwnPermission()
guest_permission = GuestPermission()
time_permission = TimePermission()


class QuestionPermission(Permission):

    def __init__(self, pid):
        need = EditQuestionNeed(int(pid))
        super(QuestionPermission, self).__init__(need)


class PostPermission(Permission):
    def __init__(self):
        score = current_user.infor.score
        need = PostNeed(score)
        super(PostPermission, self).__init__(need)

class GroupPermission(Permission):

    def __init__(self, uid):
        need = GroupNeed(int(uid))
        super(GroupPermission, self).__init__(need)


class BoardPermission(Permission):

    def __init__(self, uid):
        need = BoardNeed(int(uid))
        super(BoardPermission, self).__init__(need)


class OwnsPermission(Permission):

    def __init__(self, name):
        need = UserNameNeed(name)
        super(OwnsPermission, self).__init__(need)


class ShowPermission(Permission):

    def __init__(self, data):
        need = ShowNeed(data)
        super(ShowPermission, self).__init__(need)

super_permission = Permission(RoleNeed('super'))
admin_permission = Permission(RoleNeed('admin')).union(super_permission)
member_permission = Permission(RoleNeed('member')).union(admin_permission)
banned_permission = Permission(RoleNeed('banned')).union(member_permission)
confirm_permission = Permission(
    RoleNeed('confirm')).union(member_permission)
#  guest_permission = Permission(
    #  RoleNeed('guest')).union(confirm_permission)


show_own_permission = Permission(ShowNeed(3))
show_login_permission = Permission(ShowNeed(2)).union(show_own_permission)
show_all_permission = Permission(ShowNeed(1)).union(show_login_permission)


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    identity.user = current_user
    identity.group = Group.query.filter_by(id=34).first()

    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.name))

    if hasattr(current_user, 'is_superuser'):
        if current_user.is_superuser:
            identity.provides.add(RoleNeed('super'))

    #  if hasattr(current_user, 'is_confirmed'):
        #  if current_user.is_confirmed:
            #  identity.provides.add(PostNeed(True))

    #  if hasattr(current_user, 'questions'):
        #  for question in current_user.questions:
            #  identity.provides.add(EditQuestionNeed(int(question.id)))

    #  if hasattr(current_user, 'infor'):
        #  score = current_user.infor.score
        #  if score > 5:
            #  identity.provides.add(PostNeed(score))
        #  elif score > 1:
            #  identity.provides.add(PostNeed(score))
        #  else:
            #  pass

    #  if hasattr(current_user, 'groups'):
        #  for group in current_user.groups:
            #  identity.provides.add(GroupNeed(int(group.id)))

    #  if hasattr(Group, 'permission'):
        #  identity.provides.add(ShowNeed(identity.group.permission))
    #  print(identity)

    #  identity.provides.add(ShowNeed(1))
    #  identity.provides.add(ShowNeed(2))
    #  identity.provides.add(ShowNeed(3))
    #  print('%s\n'%identity)

    if hasattr(current_user, 'name'):
        identity.provides.add(UserNameNeed(current_user.name))
    # identity.allow_admin = admin_permission.allows(identity)
    # identity.allow_edit = editor_permission.allows(identity)
    # identity.allow_write = writer_permission.allows(identity)


class OwnPermission(object):

    def required(self, role='super'):
        def permission(func):
            @wraps(func)
            def decorator(*args, **kwargs):
                if role == 'question':
                    return self.question()
                elif role == 'replies':
                    return self.rep()
                elif role == 'super':
                    return self.superuser()
                elif role == 'own':
                    return self.own()
                elif role == 'time':
                    return self.time()
                else:
                    abort(404)
                return func(*args, **kwargs)
            return decorator
        return permission

    def question(self):
        if not confirm_permission.can():
            flash('你尚未验证账户,请尽快验证')
            return redirect(url_for('user.index',user_url=current_user.name))
        if current_user.infor.score < 5:
            flash('你的积分不足，不能发帖,如有问题请联系管理员')
            return redirect(url_for('user.index',user_url=current_user.name))

    def super(self):
        if not super_permission.can():
            abort(404)

    def admin(self):
        if not admin_permission.can():
            abort(404)

    def member(self):
        if not member_permission.can():
            abort(404)

    def banned(self):
        if not banned_permission.can():
            abort(404)

    def confirm(self):
        if not confirm_permission.can():
            flash('你尚未验证账户,请尽快验证')
            return redirect(url_for('user.index',user_url=current_user.name))
        else:
            pass

        return redirect(url_for('user.index',user_url=current_user.name))

    #  def question(self):
        #  if not confirm_permission.can():
            #  flash('你尚未验证账户,请尽快验证')
            #  return redirect(url_for('user.index',user_url=current_user.name))
        #  if current_user.infor.score < 5:
            #  flash('你的积分不足，不能发帖,如有问题请联系管理员')
            #  return redirect(url_for('user.index',user_url=current_user.name))

    def rep(self):
        if not rep_permission:
            flash('你尚未验证账户,请尽快验证')
            return redirect(url_for('user.index',user_url=current_user.name))
        else:
            pass

    def own(self,user):
        if current_user.name == user:
            pass
        else:
            abort(404)

    def time_permission(self):
        if request.method == "POST":
            user = 'user:%s' % str(current_user.id)
            last_time = redis_data.hget(user, 'send_email_time')
            now_time = int(time()) + 28800
            if not last_time:
                last_time = now_time
            else:
                last_time = int(last_time)
            if last_time > now_time - 3600:
                error = u'你的验证链接还未过期，请尽快验证'
                return error
            else:
                pass
        else:
            abort(404)

allow = OwnPermission()



# def allow_ip(user_ip):
# def decorator(f):
# @wraps(f)
# def decorated_function(*args, **kwargs):
# '''查询IP是否在黑名单中'''
# visited_users = redis_data.smembers('blacklist')
# if user_ip in visited_users:
# abort(404)
# else:
# pass
# return decorated_function
# return decorator
