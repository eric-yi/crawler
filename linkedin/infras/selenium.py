#!/usr/bin/env python
# -*- coding:utf-8 -*-


from selenium import webdriver
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, WebDriverException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


def wait_invisibility_xpath(driver, xpath, wait_timeout=None):
    if wait_timeout is None:
        wait_timeout = 3

    WebDriverWait(driver, wait_timeout).until(ec.invisibility_of_element_located((By.XPATH, xpath)))


def get_by_xpath_or_none(driver, xpath, wait_timeout=None, logs=True):
    try:
        return get_by_xpath(driver, xpath, wait_timeout=wait_timeout)
    except (TimeoutException, StaleElementReferenceException, WebDriverException) as e:
        if logs:
            print("Exception Occurred:")
            print("XPATH:%s" % xpath)
            print("Error:%s" % e)
        return None


def get_all_by_xpath_or_none(driver, xpath, wait_timeout=None, logs=True):
    try:
        return get_all_by_xpath(driver, xpath, wait_timeout=wait_timeout)
    except (TimeoutException, StaleElementReferenceException, WebDriverException) as e:
        if logs:
            print("Exception Occurred:")
            print("XPATH:%s" % xpath)
            print("Error:%s" % e)
        return None


def get_by_xpath(driver, xpath, wait_timeout=None):
    if wait_timeout is None:
        wait_timeout = 3
    return WebDriverWait(driver, wait_timeout).until(
        ec.presence_of_element_located(
            (By.XPATH, xpath)
        ))

def get_all_by_xpath(driver, xpath, wait_timeout=None):
    if wait_timeout is None:
        wait_timeout = 3
    return WebDriverWait(driver, wait_timeout).until(
        ec.presence_of_all_elements_located(
            (By.XPATH, xpath)
        ))


def init_chromium(selenium_host):
    selenium_url = 'http://%s:4444/wd/hub' % selenium_host
    print('Initializing chromium, remote url: %s' % selenium_url)
    chrome_options = DesiredCapabilities.CHROME
    prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
    chrome_options['prefs'] = prefs
    driver = webdriver.Remote(command_executor=selenium_url,
                              desired_capabilities=chrome_options)
    return driver
