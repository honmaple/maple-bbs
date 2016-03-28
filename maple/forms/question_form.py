#*************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: askform.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2015-11-27 17:54:07
#*************************************************************************
#!/usr/bin/env python
# -*- coding=UTF-8 -*-
from flask_wtf import Form
from wtforms import StringField,TextAreaField,SelectField
from wtforms.validators import Required,Length

class NoticeForm(Form):
    title = StringField('标题:',
                        [Required(message='标题不能为空'),
                         Length(min=4,
                                max=36,
                                message=u'标题长度在4到36个字符之间')])
    content = TextAreaField('问题描述:',
                            [Required(message='描述不能为空'),
                             Length(min=6,
                                    message=u'描述不能少于6个字符')])
    category = SelectField('分类',
                           choices=[('社区公告','社区公告')],
                           validators=[Required(message='分类不能为空')])
    choice = SelectField('文本标记语法',
                         choices=[('Default', 'Default'),
                                  ('Markdown', 'Markdown')])

class DevelopForm(Form):
    title = StringField('标题:',
                        [Required(message='标题不能为空'),
                         Length(min=4,
                                max=36,
                                message=u'标题长度在4到36个字符之间')])
    content = TextAreaField('问题描述:',
                            [Required(message='描述不能为空'),
                             Length(min=6,
                                    message=u'描述不能少于6个字符')])
    category = SelectField('分类',
                           choices=[('社区发展','社区发展')],
                           validators=[Required(message='分类不能为空')])
    choice = SelectField('文本标记语法',
                         choices=[('Default', 'Default'),
                                  ('Markdown', 'Markdown')])

class SuggestForm(Form):
    title = StringField('标题:',
                        [Required(message='标题不能为空'),
                         Length(min=4,
                                max=36,
                                message=u'标题长度在4到36个字符之间')])
    content = TextAreaField('问题描述:',
                            [Required(message='描述不能为空'),
                             Length(min=6,
                                    message=u'描述不能少于6个字符')])
    category = SelectField('分类',
                           choices=[('反馈建议','反馈建议')],
                           validators=[Required(message='分类不能为空')])
    choice = SelectField('文本标记语法',
                         choices=[('Default', 'Default'),
                                  ('Markdown', 'Markdown')])

class MasterForm(Form):
    title = StringField('标题:',
                        [Required(message='标题不能为空'),
                         Length(min=4,
                                max=36,
                                message=u'标题长度在4到36个字符之间')])
    content = TextAreaField('问题描述:',
                            [Required(message='描述不能为空'),
                             Length(min=6,
                                    message=u'描述不能少于6个字符')])
    category = SelectField('分类',
                           choices=[('无','无'),
                                    ('考研保研','考研保研'),
                                    ('研究生活','研究生活'),
                                    ('经验分享', '经验分享'),
                                    ('学习交流', '学习交流')],
                           validators=[Required(message='分类不能为空')])
    choice = SelectField('文本标记语法',
                         choices=[('Default', 'Default'),
                                  ('Markdown', 'Markdown')])

class NewsForm(Form):
    title = StringField('标题:',
                        [Required(message='标题不能为空'),
                         Length(min=4,
                                max=36,
                                message=u'标题长度在4到36个字符之间')])
    content = TextAreaField('问题描述:',
                            [Required(message='描述不能为空'),
                             Length(min=6,
                                    message=u'描述不能少于6个字符')])
    category = SelectField('分类',
                           choices=[('学校新闻','学校新闻'),
                                    ('物联网新闻','物联网新闻'),
                                    ('机电新闻','机电新闻'),
                                    ('企业管理新闻', '企业管理新闻'),
                                    ('研究生新闻', '研究生新闻'),
                                    ('其他新闻', '其他新闻')],
                           validators=[Required(message='分类不能为空')])
    choice = SelectField('文本标记语法',
                         choices=[('Default', 'Default'),
                                  ('Markdown', 'Markdown')])

class QuestionForm(Form):
    title = StringField('标题:',
                        [Required(message='标题不能为空'),
                         Length(min=4,
                                max=36,
                                message=u'标题长度在4到36个字符之间')])
    content = TextAreaField('问题描述:',
                            [Required(message='描述不能为空'),
                             Length(min=6,
                                    message=u'描述不能少于6个字符')])
    category = SelectField('分类',
                           choices=[('无','无'),('求助提问','求助提问'),
                                    ('经验分享','经验分享'),
                                    ('学习交流', '学习交流'),
                                    ('河海生活','河海生活')],
                           validators=[Required(message='分类不能为空')])
    choice = SelectField('文本标记语法',
                         choices=[('Default', 'Default'),
                                  ('Markdown', 'Markdown')])


class ReplyForm(Form):
    content = TextAreaField('回复:',[Required(message='回复不能为空'),
                                       Length(min=4,
                                              message=u'回复不能少于4个字符')])

class SortForm(Form):
    display = SelectField('筛选',
                          choices=[('全部主题', '全部主题'), ('1天', '1天'),
                                   ('1周','1周'),('1个月','1个月')],
                          validators=[Required(message='分类不能为空')])
    sort = SelectField('排序',choices=[('发表时间', '发表时间'),
                                         ('作者','作者')],
                       validators=[Required(message='分类不能为空')])
    st = SelectField('升降序',choices=[('降序', '降序'), ('升序', '升序')],
                     validators=[Required(message='分类不能为空')])


