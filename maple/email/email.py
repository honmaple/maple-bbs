#*************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: email.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2015-11-27 21:59:02
#*************************************************************************
#!/usr/bin/env python
# -*- coding=UTF-8 -*-
from flask_mail import Message
from threading import Thread
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from maple import app
from maple import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def email_send(to, template, subject):
    msg = Message(subject,
                  recipients=[to],
                  html=template)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()


def email_token(email):
    config = current_app.config
    serializer = URLSafeTimedSerializer(config['SECRET_KEY'])
    token = serializer.dumps(email, salt=config['SECURITY_PASSWORD_SALT'])
    return token


def confirm_token(token, expiration=10800):
    config = current_app.config
    serializer = URLSafeTimedSerializer(config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email
