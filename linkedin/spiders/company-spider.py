#!/usr/bin/env python
# -*- coding:utf-8 -*-


from scrapy.spiders import Spider

from linkedin.infras.linkedin import LinkedinOnline
from linkedin.domain.company import Company
from linkedin.conf import company


class CompanySpider(LinkedinOnline, Spider):
    name = 'company-spider'
    allowed_domains = ['www.linkedin.com']
    start_urls = ['%s%s' % ('https://www.linkedin.com/company/', company)]

    def parse(self, response):
        self.company = Company(company)
        self.company.online(self, self.driver)
        return self.company.crawl()

    def parse_employees(self, response):
        return self.company.crawl_employees(response.request.url)
