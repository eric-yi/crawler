#!/usr/bin/env python
# -*- coding:utf-8 -*-
import linkedin.domain.crawling as crawling


class TestDomainCrawling(object):
    def test_create_crawling_meta_should_be_ok(self):
        meta = crawling.CrawlingMeta(value='tests')
        assert meta.get() == 'tests'
        assert meta.origin == 'Auto'

    def test_create_crawling_data_should_ok(self):
        data = crawling.CrawlingData()
        data.set('tests')
        assert data.get() == 'tests'

    def test_create_crawling_should_ok(self):
        c = crawling.Crawling()

        assert c.status.get() == crawling.Status.Lose
