# *************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: articledb.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2015-11-29 02:07:53
# *************************************************************************
# !/usr/bin/env python
# -*- coding=UTF-8 -*-
from maple import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, \
    check_password_hash

ROLES = [('super', 'super'), ('admin', 'admin'),
         ('member', 'member'), ('unconfirmed', 'unconfirmed'),
         ('visitor', 'visitor')]


class Permission(db.Model):
    '''
    admin_manager:admin_post,admin_edit,admin_read,admin_delete
    que_manager:que_post,que_edit,que_read,que_delete
    rep_manager:rep_post,rep_edit,rep_read,rep_delete
    own_manager:update_password,update_infor,own_read
    '''
    __tablename__ = 'permission'
    id = db.Column(db.Integer, primary_key=True)
    percode = db.Column(db.String(81), nullable=False)
    pername = db.Column(db.String(81), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    module_id = db.Column(db.Integer,
                          db.ForeignKey('modules.id',
                                        ondelete="CASCADE"))
    module = db.relationship('Module',
                             backref=db.backref('permission',
                                                cascade='all,delete-orphan',
                                                lazy='dynamic'))
    roles = db.relationship('Role',
                            secondary='role_permission',
                            backref=db.backref('permission',
                                               lazy='dynamic'))


class Module(db.Model):
    '''
    后台管理:admin_manager
    问题管理:que_manager
    回复管理:rep_manager
    个人管理:own_manager
    '''
    __tablename__ = 'modules'
    id = db.Column(db.Integer, primary_key=True)
    modulecode = db.Column(db.String(81), unique=True)
    modulename = db.Column(db.String(81), unique=True)
    parentcode = db.Column(db.String(81), nullable=True)
    moduleurl = db.Column(db.String(81), nullable=True)


class UserRole(db.Model):
    __tablename__ = 'user_role'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    roles_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


class RolePermission(db.Model):
    __tablename__ = 'role_permission'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'))


class Role(db.Model):
    '''
     super
     admin
     member
     banned
     unconfirmed
     guest
     group_admin
     board_admin
    '''
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(81), nullable=False,default='unconfirmed')
    description = db.Column(db.String(255), nullable=True)
    rank = db.Column(db.Integer,nullable=False,default=1)
    users = db.relationship('User',
                            secondary='user_role',
                            backref=db.backref('roles',
                                               lazy='dynamic'))
    __mapper_args__ = {"order_by": rank.desc()}


class UserInfor(db.Model):
    __tablename__ = 'userinfor'
    id = db.Column(db.Integer, primary_key=True)
    confirmed_time = db.Column(db.DateTime, nullable=True)
    registered_time = db.Column(db.DateTime, nullable=False)
    score = db.Column(db.Integer, nullable=False, default=100)
    word = db.Column(db.Text, nullable=True)
    introduce = db.Column(db.Text, nullable=True)
    school = db.Column(db.String, nullable=True)
    count_id = db.Column(db.Integer,
                         db.ForeignKey('counts.id',
                                       ondelete="CASCADE"))
    count = db.relationship("Counts",
                            backref="user",
                            cascade='all,delete-orphan',
                            single_parent=True,
                            uselist=False)

    def __init__(self):
        self.registered_time = datetime.now()

    def __repr__(self):
        return "<UserInfor %r>" % self.id


class UserSetting(db.Model):
    '''
    1:all user
    2:logined user
    3:only own
    '''
    __tablename__ = 'usersetting'
    id = db.Column(db.Integer, primary_key=True)
    online_status = db.Column(db.Integer, nullable=False, default=1)
    topic_list = db.Column(db.Integer, nullable=False, default=1)
    rep_list = db.Column(db.Integer, nullable=False, default=1)
    ntb_list = db.Column(db.Integer, nullable=False, default=3)
    collect_list = db.Column(db.Integer, nullable=False, default=2)

    def __repr__(self):
        return "<UserSetting %r>" % self.id


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, )
    name = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    passwd = db.Column(db.String, nullable=False)
    #  roles = db.Column(db.String, nullable=False, default='visitor')
    is_superuser = db.Column(db.Boolean, default=False)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)

    setting_id = db.Column(db.Integer,
                           db.ForeignKey('usersetting.id',
                                         ondelete="CASCADE"))
    setting = db.relationship("UserSetting",
                              backref="users",
                              cascade='all,delete',
                              uselist=False)

    infor_id = db.Column(db.Integer,
                         db.ForeignKey('userinfor.id',
                                       ondelete="CASCADE"))
    infor = db.relationship("UserInfor",
                            backref="users",
                            cascade='all,delete',
                            uselist=False)

    def __init__(self, name, email, passwd):
        self.name = name
        self.email = email
        self.passwd = self.set_password(passwd)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_auth_token(self):
        from maple import login_serializer
        data = [self.name, self.passwd]
        return login_serializer.dumps(data)

    def __repr__(self):
        return "<User %r>" % self.name

    @staticmethod
    def load_by_id(uid):
        user = User.query.filter_by(id=uid).first()
        return user

    @staticmethod
    def load_by_name(name):
        user = User.query.filter_by(name=name).first()
        return user

    @staticmethod
    def load_by_email(email):
        user = User.query.filter_by(email=email).first()
        return user

    @staticmethod
    def check_password(user_password, password):
        return check_password_hash(user_password, password)
