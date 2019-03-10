#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
from scrapy import Request
from linkedin.domain.crawling import CrawlingData, Crawling
import linkedin.infras.utils as utils


class Directory(Crawling):
    def __init__(self, link):
        self.link = link
        super().__init__()

    def _load_persistent(self):
        super()._load_persistent()
        self.mongo.set_db('linkedin-directory')
        self.table = 'person-%s-homepage-%s' % (self.link[-1], utils.gen_timestamp())

    def crawl(self):
        logging.debug('==== directory crawl...')
        self.total = self._extract_total()
        logging.debug('==== directory number: %s' % self.total)
        self.position = 0
        return self._handle_person_url()

    def crawl_person(self):
        logging.debug('==== person crawl...')
        homepages = self._crawl_all_link('.//li[@class="content"]')
        self._handle_homepages(homepages)
        self.position = self.position + 1
        return self._handle_person_url()

    def _extract_total(self):
        context = self._crawl_all('.//div[@class="section bucket-container"]')[1]
        return len(self._crawl_all_with(context, './/li[@class="bucket-item"]'))

    def _handle_person_url(self):
        self.position = self.position + 1
        if self.position <= self.total:
            url = '%s-%s' % (self.link, self.position)
            return Request(url=url,
                           callback=self.spider.parse_person,
                           dont_filter=True,
                           )
        else:
            return

    def _handle_homepages(self, homepages):
        for homepage in homepages:
            homepage = homepage[:-len('?trk=people_directory')]
            logging.debug('==== homepage : %s ' % homepage)
            self.mongo.insert(self.table, {'homepage': homepage})
