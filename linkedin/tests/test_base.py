#!/usr/bin/env python
# -*- coding:utf-8 -*-

from linkedin.infras.linkedin import LinkedinOnline


class TestLinkedin(object):
    def setup(self):
        self.online = LinkedinOnline('localhost')

    def teardown(self):
        self.online.close()
