#!/usr/bin/env python
# -*- coding:utf-8 -*-
from linkedin.infras.mongodb import Mongodb


class TestInfrasMongodb(object):
    def setup(self):
        self.mongo = Mongodb('127.0.0.1', 27017)
        self.mongo.set_db('tests')

    def test_create_should_connect_to_server(self):
        assert self.mongo.client is not None
        assert self.mongo.db is not None

    def test_insert_should_ok(self):
        self.mongo.insert('tests', {"n1": "1", "n2": 2})
        assert True

    def test_get_should_ok(self):
        dataset = self.mongo.get('tests')
        assert dataset is not None
        if len(dataset) > 0:
            assert dataset[0] is not None

    def test_list_tables_should_get_index_tables(self):
        tables = self.mongo.list_tables()
        if len(tables) > 0:
            assert tables[0] is not None
