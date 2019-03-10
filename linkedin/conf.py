#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logging.getLogger('scrapy').setLevel(logging.WARNING)
logging.getLogger('selenium').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

EMAIL = ''
PASSWORD = ''

company = '**'
logs = 'logs'

mongodb = {
    'host': '127.0.0.1',
    'port': 27017
}
