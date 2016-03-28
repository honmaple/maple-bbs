#*************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: cd.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2015-11-22 04:11:03
#*************************************************************************
#!/usr/bin/env python
# -*- coding=UTF-8 -*-
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from flask import session
from io import BytesIO


class ValidateCode(object):
    _letter_cases = "abcdefghjkmnpqrstuvwxy"  # 小写字母，去除可能干扰的i，l，o，z
    _upper_cases = _letter_cases.upper()  # 大写字母
    _numbers = ''.join(map(str, range(3, 10)))  # 数字
    init_chars = ''.join((_letter_cases, _upper_cases, _numbers))
    fontType = "/usr/share/fonts/TTF/DejaVuSans.ttf"

    def create_validate_code(self, size=(120, 30),
                             chars=init_chars,
                             img_type="GIF",
                             mode="RGB",
                             bg_color=(255, 255, 255),
                             fg_color=(0, 0, 255),
                             font_size=18,
                             font_type=fontType,
                             length=4,
                             draw_lines=True,
                             n_line=(1, 2),
                             draw_points=True,
                             point_chance=2):

        width, height = size  # 宽， 高
        img = Image.new(mode, size, bg_color)  # 创建图形
        draw = ImageDraw.Draw(img)  # 创建画笔
        if draw_lines:
            self.create_lines(draw, n_line, width, height)
        if draw_points:
            self.create_points(draw, point_chance, width, height)
            strs = self.create_strs(draw,
                                    chars,
                                    length,
                                    font_type,
                                    font_size,
                                    width,
                                    height,
                                    fg_color)

        # 图形扭曲参数
        params = [1 - float(random.randint(1, 2)) / 100,
                  0,
                  0,
                  0,
                  1 - float(random.randint(1, 10)) / 100,
                  float(random.randint(1, 2)) / 500,
                  0.001,
                  float(random.randint(1, 2)) / 500
                  ]
        img = img.transform(size, Image.PERSPECTIVE, params)  # 创建扭曲

        img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强（阈值更大）

        return img, strs

    def create_lines(self, draw, n_line, width, height):
        '''绘制干扰线'''
        line_num = random.randint(n_line[0], n_line[1])  # 干扰线条数
        for i in range(line_num):
            # 起始点
            begin = (random.randint(0, width), random.randint(0, height))
            # 结束点
            end = (random.randint(0, width), random.randint(0, height))
            draw.line([begin, end], fill=(0, 0, 0))

    def create_points(self, draw, point_chance, width, height):
        '''绘制干扰点'''
        chance = min(100, max(0, int(point_chance)))  # 大小限制在[0, 100]

        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    def create_strs(
        self,
        draw,
        chars,
        length,
        font_type,
        font_size,
        width,
        height,
     fg_color):
        '''绘制验证码字符'''
        '''生成给定长度的字符串，返回列表格式'''
        c_chars = random.sample(chars, length)
        strs = ' %s ' % ' '.join(c_chars)  # 每个字符前后以空格隔开

        font = ImageFont.truetype(font_type, font_size)
        font_width, font_height = font.getsize(strs)

        draw.text(((width - font_width) / 3, (height - font_height) / 3), strs,
                  font=font, fill=fg_color)

        return ''.join(c_chars)

    def start(self):
        code_img = self.create_validate_code()
        buf = BytesIO()
        code_img[0].save(buf, 'JPEG', quality=70)
        session['validate_code'] = code_img[1]
        return buf
