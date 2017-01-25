#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: utils.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-01-25 21:39:41 (CST)
# Last Update:星期三 2017-1-25 21:43:0 (CST)
#          By:
# Description:
# **************************************************************************
import traceback
import logging
from functools import wraps
from .response import HTTPResponse

logger = logging.getLogger("logg")


def log_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logger.info(str(args))
            logger.info(str(kwargs))
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            error = traceback.format_exc()
            logger.info(u"cache unhanld exception%s ", error)
            return HTTPResponse(
                HTTPResponse.OTHER_ERROR,
                description=u"捕获到未处理的异常,%s" % error).to_response()

    return wrapper
