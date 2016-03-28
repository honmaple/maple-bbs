#*************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: academy.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2016-02-07 12:34:33
#*************************************************************************
#!/usr/bin/env python
# -*- coding=UTF-8 -*-
from flask import render_template, Blueprint, flash, request, g, abort, jsonify,\
    redirect, url_for, session, current_app
from flask_login import logout_user, current_user, login_required
from flask_principal import AnonymousIdentity, \
     identity_changed
from werkzeug.security import generate_password_hash
from maple.question.models import Questions, Replies, Collector
from maple.user.models import User, UserSetting,Role,Permission
from maple.user.forms import SettingForm, NewPasswdForm, PrivacyForm
from maple.group.models import Message
from maple.main.permissions import own_permission
from maple.forms.forms import return_errors
from maple import redis_data, db

site = Blueprint('user', __name__)


@site.url_value_preprocessor
def pull_user_url(endpoint, values):
    url = values.pop('user_url')
    g.user_url = url


@site.url_defaults
def add_user_url(endpoint, values):
    if 'user_url' in values or not g.user_url:
        return
    values['user_url'] = g.user_url


@site.route('')
def index():
    user = User.query.filter_by(name=g.user_url).first_or_404()
    if g.user is not None and g.user.is_authenticated:
        user_count = redis_data.hget('user:%s' % str(current_user.id), 'topic')
        if not user_count:
            user_count = 0
        else:
            user_count = int(user_count)
        return render_template('user/user.html',
                               user_count=user_count,
                               category='',
                               user=user)
    else:
        return render_template('user/user.html', user=user, category='')


@site.route('/<category>', defaults={'number': 1})
@site.route('/<category>&page=<int:number>')
def category(category, number):
    user = User.query.filter_by(name=g.user_url).first_or_404()
    user_count = redis_data.hget('user:%s' % str(user.id), 'topic')
    if not user_count:
        user_count = 0
    else:
        user_count = int(user_count)
    return render_template('user/user.html',
                           user=user,
                           category=category,
                           user_count=user_count)


@site.route('/settings', methods=['GET', 'POST'])
@login_required
@own_permission
def setting():
    '''用户设置'''
    error = None
    form = SettingForm()
    passwd_form = NewPasswdForm()
    mode = request.args.get('mode')
    if mode == 'setting':
        if form.validate_on_submit() and request.method == "POST":
            introduce = form.introduce.data
            school = form.school.data
            word = form.word.data
            current_user.infor.introduce = introduce
            current_user.infor.school = school
            current_user.infor.word = word
            db.session.commit()
            flash('资料更新成功')
            return jsonify(judge=True, error=error)
        else:
            if form.errors:
                return return_errors(form)
            else:
                pass
            return redirect(url_for('user.setting'))
    elif mode == 'password':
        if passwd_form.validate_on_submit() and request.method == "POST":
            user = User.query.filter_by(name=current_user.name).first()
            passwd = passwd_form.passwd.data
            rpasswd = passwd_form.rpasswd.data
            if not User.check_password(user.passwd, passwd):
                error = u'密码错误'
                return jsonify(judge=False, error=error)
            else:
                user.passwd = generate_password_hash(rpasswd)
                db.session.commit()
                logout_user()
                session.clear()
                for key in ('identity.id', 'identity.auth_type'):
                    session.pop(key, None)
                identity_changed.send(current_app._get_current_object(),
                                      identity=AnonymousIdentity())
                flash('密码修改成功,请重新登陆')
                return jsonify(judge=True, error=error)
        else:
            if passwd_form.passwd.errors:
                error = passwd_form.passwd.errors
                return jsonify(judge=False, error=error)
            elif passwd_form.npasswd.errors:
                error = passwd_form.npasswd.errors
                return jsonify(judge=False, error=error)
            else:
                return redirect(url_for('user.setting'))
    else:
        form.school.data = current_user.infor.school
        form.word.data = current_user.infor.word
        form.introduce.data = current_user.infor.introduce
        return render_template('user/user_settings.html',
                               category=category,
                               passwd_form=passwd_form,
                               form=form)


@site.route('/settings/privacy', methods=['GET', 'POST'])
@login_required
@own_permission
def privacy():
    error = None
    form = PrivacyForm()
    if form.validate_on_submit() and request.method == "POST":
        online_status = form.online_status.data
        topic_list = form.topic_list.data
        rep_list = form.rep_list.data
        ntb_list = form.ntb_list.data
        collect_list = form.collect_list.data
        current_user.setting.online_status = online_status
        current_user.setting.topic_list = topic_list
        current_user.setting.rep_list = rep_list
        current_user.setting.ntb_list = ntb_list
        current_user.setting.collect_list = collect_list
        db.session.commit()
        flash('更新成功')
        return jsonify(judge=True, error=error)
    else:
        if form.errors:
            return return_errors(form)
        else:
            pass
        form.online_status.data =  current_user.setting.online_status
        form.topic_list.data = current_user.setting.topic_list
        form.rep_list.data = current_user.setting.rep_list
        form.ntb_list.data = current_user.setting.ntb_list
        form.collect_list.data = current_user.setting.collect_list
        return render_template('user/user_privacy.html', form=form)


@site.route('/daily')
@login_required
@own_permission
def daily():
    '''签到'''
    user = 'user' + ':' + 'daily' + ':' + str(current_user.id)
    if redis_data.exists(user):
        flash('你已签到,不能重复签到')
        return redirect(url_for('user.index', user_url=current_user.name))
    else:
        from datetime import date, timedelta
        from time import mktime
        today = date.today() + timedelta(days=1)
        a = mktime(today.timetuple())
        b = a + 28800
        pipe = redis_data.pipeline()
        pipe.set(user, '1')
        pipe.expireat(user, int(b))
        pipe.execute()
        current_user.infor.score += 10
        db.session.commit()
        flash('签到成功')
        return redirect(url_for('user.index', user_url=current_user.name))


@site.route('/notices')
@login_required
@own_permission
def notice():
    '''未读提醒'''
    user = 'user:%s' % str(current_user.id)
    redis_data.hset(user, 'notice', 0)
    messages = Message.query.filter_by(rece_user=current_user.name).all()
    return render_template('user/user_notice.html', messages=messages)
