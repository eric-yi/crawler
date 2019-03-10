#!/usr/bin/env python
# -*- coding:utf-8 -*-

from datetime import datetime
import uuid
import os
import json


def gen_serial():
    return str(uuid.uuid4())


def gen_timestamp():
    return datetime.now().timestamp()


def mkdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir


def to_json(dict):
    return json.dumps(dict)
