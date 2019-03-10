#!/usr/bin/env python
# -*- coding:utf-8 -*-

import random
import logging
from scrapy.http import Response
from linkedin.agents import AGENTS
import linkedin.infras.selenium as selenium


class LoadingMiddleware:
    def process_request(self, request, spider):
        try:
            driver = spider.driver
            print('SeleniumMiddleware - getting the page')
            driver.get(request.url)
            logging.info('==== PageLoading url: %s' % request.url)
            if spider.loading:
                print('waiting for page loading')
                profile_xpath = "//*[@id='nav-settings__dropdown-trigger']/img"
                selenium.get_by_xpath(driver, profile_xpath)
                print('SeleniumMiddleware - retrieving body')
            return Response(driver.current_url)
        except Exception as e:
            logging.error('==== Error: PageLoading %s' % e)

class AgentMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(AGENTS)
        request.headers['User-Agent'] = agent
