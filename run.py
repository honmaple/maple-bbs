# *************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: run.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2016-02-07 09:12:47
# *************************************************************************
# !/usr/bin/env python
# -*- coding=UTF-8 -*-
from maple import app
from werkzeug.contrib.fixers import ProxyFix

app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == '__main__':
    #  import logging
    #  logFormatStr = '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
    #  logging.basicConfig(format = logFormatStr, filename = "global.log", level=logging.DEBUG)
    #  formatter = logging.Formatter(logFormatStr,'%m-%d %H:%M:%S')
    #  fileHandler = logging.FileHandler("summary.log")
    #  fileHandler.setLevel(logging.DEBUG)
    #  fileHandler.setFormatter(formatter)
    #  streamHandler = logging.StreamHandler()
    #  streamHandler.setLevel(logging.DEBUG)
    #  streamHandler.setFormatter(formatter)
    #  app.logger.addHandler(fileHandler)
    #  app.logger.addHandler(streamHandler)
    #  app.logger.info("Logging is set up.")
    app.run()
