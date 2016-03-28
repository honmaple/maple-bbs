# *************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: auth.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2015-11-25 02:21:04
# *************************************************************************
# !/usr/bin/env python
# -*- coding=UTF-8 -*-
from flask import (render_template,
                   Blueprint,
                   redirect,
                   url_for,
                   flash,
                   request,
                   current_app,
                   session,
                   abort,
                   jsonify)
from flask_login import (login_user,
                         logout_user,
                         current_user,
                         login_required)
from flask_principal import (Identity, AnonymousIdentity,
                             identity_changed)
from werkzeug.security import generate_password_hash
from maple import redis_data, app, db
from maple.main.permissions import guest_permission, time_permission
from maple.email.email import email_token, email_send, confirm_token
from maple.user.models import User, UserInfor, UserSetting, Role
from maple.auth.forms import LoginForm, RegisterForm, ForgetPasswdForm
from maple.forms.forms import return_errors
from datetime import datetime

site = Blueprint('auth', __name__)


@site.route('/login', methods=['GET', 'POST'])
@guest_permission
def login():
    error = None
    form = LoginForm()
    if form.validate_on_submit() and request.method == "POST":
        validate_code = session['validate_code']
        validate = form.code.data
        if validate.lower() != validate_code.lower():
            return jsonify(judge=False, error=u'验证码错误')
        else:
            name = form.name.data
            passwd = form.passwd.data
            remember = request.get_json()["remember"]
            user = User.load_by_name(name)
            if user and User.check_password(user.passwd, passwd):
                if remember:
                    session.permanent = True

                login_user(user, remember=remember)

                identity_changed.send(current_app._get_current_object(),
                                      identity=Identity(user.id))
                flash(u'你已成功登陆')
                return jsonify(judge=True, error=error)
            else:
                error = u'用户名或密码错误'
                return jsonify(judge=False, error=error)
    else:
        if form.errors:
            return return_errors(form)
        else:
            pass
        return render_template('auth/login.html', form=form, error=error)


@site.route('/logout')
@login_required
def logout():
    '''注销'''
    logout_user()
    session.clear()
    for key in ('identity.id', 'identity.auth_type'):
        session.pop(key, None)
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())
    return redirect(request.args.get('next') or url_for('forums.forums'))


@site.route('/register', methods=['GET', 'POST'])
@guest_permission
def register():
    error = None
    form = RegisterForm()
    if form.validate_on_submit() and request.method == "POST":
        validate_code = session['validate_code']
        validate = form.code.data
        if validate.lower() != validate_code.lower():
            return jsonify(judge=False, error=u'验证码错误')
        else:
            useremail = User.load_by_email(form.email.data)
            username = User.load_by_name(form.name.data)
            if username is not None:
                error = u'用户名已存在'
                return jsonify(judge=False, error=error)
            elif useremail is not None:
                error = u'邮箱已被注册'
                return jsonify(judge=False, error=error)
            else:
                account = User(name=form.name.data,
                               email=form.email.data,
                               passwd=form.passwd.data)
                userinfor = UserInfor()
                usersetting = UserSetting()
                roles = Role(name='unconfirmed', rank=1)
                account.infor = userinfor
                account.setting = usersetting
                account.roles.append(roles)
                '''邮箱验证'''
                token = email_token(account.email)
                confirm_url = url_for('auth.confirm',
                                      token=token,
                                      _external=True)
                html = render_template('templet/email.html',
                                       confirm_url=confirm_url)
                subject = "请验证你的邮箱"
                email_send(account.email, html, subject)

                db.session.add(account)
                db.session.commit()
                '''记录用户数'''
                redis_data.hincrby('user', 'all:count', 1)

                login_user(account)
                identity_changed.send(current_app._get_current_object(),
                                      identity=Identity(account.id))
                '''发送邮件时间'''
                from time import time
                time = int(time()) + 28800
                user = 'user:%s' % str(current_user.id)
                redis_data.hset(user, 'send_email_time', time)
                flash(u'一封验证邮件已发往你的邮箱，請查收.')
                return jsonify(judge=True, error=error)
    else:
        if form.errors:
            return return_errors(form)
        else:
            pass
        if request.args.get('mode') == 'agree':
            return render_template('auth/register.html',
                                   form=form,
                                   error=error)
        else:
            return render_template('auth/register_service.html',
                                   form=form,
                                   error=error)


@site.route('/confirm/<token>')
@login_required
def confirm(token):
    email = confirm_token(token)
    if not email:
        flash('验证链接已过期,请重新获取', 'danger')
        return redirect(url_for('user.index', user_url=current_user.name))
    user = User.query.filter_by(email=email).first()
    if user.is_confirmed:
        flash('账户已经验证. Please login.', 'success')
    else:
        user.is_confirmed = True
        user.confirmed_time = datetime.now()
        role = Role(name='member', rank=3)
        user.roles.append(role)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('forums.forums'))


@site.route('/confirm_email', methods=['GET', 'POST'])
@login_required
def confirm_email():
    if request.method == "POST":
        if not time_permission.allow():
            return time_permission.action()
        else:
            token = email_token(current_user.email)
            '''email模板'''
            confirm_url = url_for('auth.confirm', token=token, _external=True)
            html = render_template(
                'templet/email.html',
                confirm_url=confirm_url)
            subject = "Please confirm your email"
            email_send(current_user.email, html, subject)
            from time import time
            time = int(time()) + 28800
            user = 'user:%s' % str(current_user.id)
            redis_data.hset(user, 'send_email_time', time)
            error = '一封验证邮件已发往你的邮箱，請查收.'
            return error
    else:
        abort(404)


@site.route('/forget', methods=['GET', 'POST'])
def forget():
    '''忘记密码'''
    error = None
    form = ForgetPasswdForm()
    if form.validate_on_submit() and request.method == "POST":
        validate_code = session['validate_code']
        validate = form.code.data
        if validate.lower() != validate_code.lower():
            return jsonify(judge=False, error=u'验证码错误')
        else:
            exsited_email = User.query.filter_by(
                email=form.confirm_email.data).first()
            if exsited_email:
                '''email模板'''
                from random import sample
                from string import ascii_letters, digits
                npasswd = ''.join(sample(ascii_letters + digits, 8))
                exsited_email.passwd = generate_password_hash(npasswd)
                db.session.commit()
                html = render_template('templet/forget.html',
                                       confirm_url=npasswd)
                subject = "请及时修改你的密码"
                email_send(form.confirm_email.data, html, subject)
                flash(u'邮件已发送到你的邮箱,请及时查收并修改密码')
                return jsonify(judge=True, error=error)
            else:
                error = u'邮箱未注册'
                return jsonify(judge=False, error=error)
    else:
        if form.errors:
            return return_errors(form)
        else:
            pass
        return render_template('auth/forget.html', form=form)


@site.route('/validcode', methods=['GET'])
def validcode():
    from maple.main.validate_code import ValidateCode
    t = ValidateCode()
    buf = t.start()
    buf_value = buf.getvalue()
    response = app.make_response(buf_value)
    response.headers['Content-Type'] = 'image/jpeg'
    return response
