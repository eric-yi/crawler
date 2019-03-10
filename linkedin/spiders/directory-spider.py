#!/usr/bin/env python
# -*- coding:utf-8 -*-


from scrapy.spiders import Spider

from linkedin.infras.linkedin import LinkedinOnline
from linkedin.domain.directory import Directory


class DirectorySpider(LinkedinOnline, Spider):
    name = 'directory-spider'
    allowed_domains = ['www.linkedin.com']
    start_urls = ['https://www.linkedin.com/directory/people-%s' % s
                  for s in 'abcdefghijklmnopqrstuvwxyz']
    start_urls = [start_urls[0]]
    loading = False

    def parse(self, response):
        print('==== url: %s ' % response.request.url)
        self.directory = Directory(response.request.url)
        self.directory.online(self, self.driver)
        return self.directory.crawl()

    def parse_person(self, response):
        return self.directory.crawl_person()