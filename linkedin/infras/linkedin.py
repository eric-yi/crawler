#!/usr/bin/env python
# -*- coding:utf-8 -*-


import linkedin.infras.selenium as selenium
import linkedin.conf as conf


class LinkedinOnline:
    loading = True
    
    def __init__(self, selenium_hostname=None, **kwargs):
        if selenium_hostname is None:
            selenium_hostname = 'selenium'
        self.driver = selenium.init_chromium(selenium_hostname)
        self.login()
        super().__init__(**kwargs)

    def login(self):
        self.driver.get('https://www.linkedin.com/')
        print('Searching for the Login btn')
        selenium.get_by_xpath(self.driver, '//*[@class="login-email"]').send_keys(conf.EMAIL)
        print('Searching for the password btn')
        selenium.get_by_xpath(self.driver, '//*[@class="login-password"]').send_keys(conf.PASSWORD)
        print('Searching for the submit')
        selenium.get_by_xpath(self.driver, '//*[@id="login-submit"]').click()

    def closed(self, reason):
        self.driver.close()
