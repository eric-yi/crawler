#!/usr/bin/env python
# -*- coding:utf-8 -*-


from scrapy.spiders import Spider

from linkedin.infras.linkedin import LinkedinOnline
from linkedin.domain.company import Company
from linkedin.conf import company


class EmployeeSpider(LinkedinOnline, Spider):
    name = 'employee-spider'
    allowed_domains = ['www.linkedin.com']
    company = Company(company)
    start_urls = []
    url_map = {}
    for employee in company.find_valid_employees():
        start_urls.append(employee.brief.homepage.get())
        url_map[employee.brief.homepage.get()] = employee
    print('==== employee spdier to crawl %s employees' % len(start_urls))

    # if len(start_urls) > 0:
    #     start_urls = [start_urls[0]]

    def parse(self, response):
        try:
            employee = self.url_map[response.request.url]
            employee.online(self, self.driver)
            employee.crawl()
        except Exception as e:
            print('==== Error: employee %s parser: %s' % (response.request.url, e))
