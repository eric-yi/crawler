#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pymongo


class Mongodb(object):
    def __init__(self, host, port):
        self.client = pymongo.MongoClient(host, port)

    def set_db(self, db):
        self.db = self.client[db]

    def insert(self, table, value):
        self.db[table].insert_one(value)

    def get(self, table):
        return self.db[table].find()

    def list_tables(self):
        return self.db.list_collection_names()
