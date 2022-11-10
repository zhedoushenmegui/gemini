#!/usr/bin/env python
"""
author: lemon
create date: 2022/4/14
description:
history:
    lemon    init
"""

# import sys
# import os
# project_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))
# sys.path.append(project_path)
import logging
from logging.handlers import TimedRotatingFileHandler
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

logger = logging.getLogger()


def set_logger(log_path, level=INFO):
    log_formatter = logging.Formatter('%(asctime)s [%(funcName)s: %(filename)s,%(lineno)d] %(levelname)s: %(message)s')
    log_handler = TimedRotatingFileHandler(log_path, when="midnight", backupCount=7)
    log_handler.suffix = "%Y%m%d"
    log_handler.setFormatter(log_formatter)
    logger.addHandler(log_handler)
    if level not in {DEBUG, INFO, WARNING, ERROR, CRITICAL}:
        level = INFO
    logger.setLevel(level)
