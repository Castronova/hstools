#!/usr/bin/env python3

import sys
import logging

format = '%(message)s'
formatter = logging.Formatter(fmt=format)
logger = logging.getLogger('root')
logger.setLevel(logging.INFO)
logger.propagate = False
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

def set_verbose():
    logger.setLevel(logging.INFO)

def set_quiet():
    logger.setLevel(logging.ERROR)
