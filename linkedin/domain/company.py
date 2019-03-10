#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import time
from scrapy import Request
import linkedin.conf as conf
from linkedin.domain.crawling import CrawlingData, Crawling
from linkedin.domain.employee import Employee
import linkedin.infras.utils as utils


class Company(Crawling):
    def __init__(self, name):
        self.name = self._create_with(name)
        self.website = self._create()
        self.location = self._create()
        self._employees = []
        super().__init__()

    def _load_persistent(self):
        self.table = 'employee-index-%s' % utils.gen_timestamp()
        employees_index = os.path.join(utils.mkdir(os.path.join(conf.logs, self.name.get())), self.table)
        self.employees_store = open(employees_index, 'w')
        super()._load_persistent()
        self.mongo.set_db(self.name.get())

    def find_valid_employees(self):
        index_table = self._get_index()
        if index_table is None:
            return []
        dataset = self.mongo.get(index_table)
        employees = []
        for data in dataset:
            if data['id']['value'] != 'unkown':
                employee = Employee()
                employee.load_brief(data)
                employee.index = index_table[len('employee-index-'):]
                employees.append(employee)
        return employees

    def _get_index(self):
        index_tables = list(filter(lambda table: 'employee-index' in table, self.mongo.list_tables()))
        index_tables.sort(key=lambda table: table[len('employee-index'):], reverse=True)
        if len(index_tables) > 0:
            return index_tables[0]
        return None

    def crawl(self):
        url = '%s%s' % (self._employees_link(), '&page=1')
        return Request(url=url,
                       callback=self.spider.parser_employees,
                       dont_filter=True,
                       )

    def _employees_link(self):
        print('Searching for the "See all * employees on LinkedIn" btn')
        xpath = '//a/strong[starts-with(text(),"See all")]'
        link = self._crawl_link(xpath)
        print('Found the following URL: %s' % link)
        return link

    def crawl_employees(self, url):
        print('Now parsing search result page')
        context = self._crawl('//*[text()="No results found."]')
        if context is not None:
            print('"No results" message shown, stop crawling this company')
            return
        else:
            employees = self._extract_employees()
            self._handle_employees(employees, url)
            return self._crawl_next_employees(url)

    def _extract_employees(self):
        xpath = '//li[@class="search-s-facet search-s-facet--facetCurrentCompany inline-block ' \
                'search-s-facet--is-closed ember-view"]/form/button/div/div/h3 '
        name = self._crawl_data(xpath)
        print('Company:%s' % name)
        employees = []
        for i in range(1, 11):
            print('loading %sth user' % i)
            context = self._crawl('//li[%s]/div/div[@class="search-result__wrapper"]' % i)
            if context is not None:
                employee = self._extract_employee(context)
                employees.append(employee)
                context = self._crawl('.//figure[@class="search-result__image"]/img')
                if context is not None:
                    self.context.execute_script("arguments[0].scrollIntoView();", context)
            time.sleep(0.7)
        return employees

    def _extract_employee(self, context):
        employee = Employee()
        employee.set_brief('company', self.name.get())
        name = self._crawl_data_with(context, './/*[@class="name actor-name"]')
        employee.set_brief('name', name)
        title = self._crawl_data_with(context, './/p')
        employee.set_brief('title', title)
        if name not in (None, 'LinkedIn Member'):
            homepage = self._crawl_link_with(context,
                                             './/*[@class="search-result__result-link search-result__result-link--visited ember-view"]')
            employee.set_brief('homepage', homepage)
            try:
                id = homepage.split('/')[-2]
                employee.set_brief('id', id)
            except Exception as e:
                print(e)
        return employee

    def _handle_employees(self, employees, url):
        indeies = []
        serial = utils.gen_serial()
        timestamp = utils.gen_timestamp()
        for employee in employees:
            employee.brief.set_serial_with(serial)
            employee.brief.set_timestamp_with(timestamp)
            employee.brief.set_origin_with(url)
            data = employee.brief.values()
            self.mongo.insert(self.table, data)
            del data['_id']
            indeies.append(data)
        print('==== indeies = %s' % indeies)
        self.employees_store.write(utils.to_json(indeies))
        self.employees_store.write('\n')
        self.employees_store.flush()

    def _crawl_next_employees(self, url):
        next_url_split = url.split('=')
        index = int(next_url_split[-1])
        next_url = '='.join(next_url_split[:-1]) + '=' + str(index + 1)
        return Request(url=next_url,
                       callback=self.spider.parse_employees,
                       meta={'company': self.name.get()},
                       dont_filter=True,
                       )
