#!/usr/bin/env python
# -*- coding:utf-8 -*-

from enum import Enum
import collections
import linkedin.infras.utils as utils
import linkedin.infras.selenium as selenium
from linkedin.infras.mongodb import Mongodb
import linkedin.conf as conf


class Status(Enum):
    Lose = 0
    Part = 1
    Full = 2


class CrawlingMeta(object):
    def __init__(self, **kwargs):
        self._default()
        for var in self.__dict__:
            if var in kwargs:
                setattr(self, var, kwargs[var])

    def _default(self):
        self.serial = utils.gen_serial()
        self.timestamp = utils.gen_timestamp()
        self.origin = 'Auto'
        self.value = None

    def get(self):
        return self.value

    def set(self, value):
        self.value = value

    def values(self):
        return {'serial': str(self.serial),
                'timestamp': str(self.timestamp),
                'origin': str(self.origin),
                'value': str(self.value)
                }


class CrawlingData(object):
    def __init__(self):
        self.current = CrawlingMeta()
        self.history = []

    def set(self, value):
        self.current.set(value)

    def get(self):
        return self.current.get()


class Crawling(object):
    def __init__(self):
        self.status = self._create_with(Status.Lose)
        self._persistent_loaded = False
        self._load_persistent()

    def _create(self):
        return self._create_with('unkown')

    def _create_with(self, value):
        data = CrawlingData()
        data.set(value=value)
        return data

    def set(self, var, val):
        self.__dict__[var].set(val)

    def get(self, var):
        return self.__dict__[var].get()

    def values(self):
        values = {}
        for var in self.__dict__:
            self._values(values, self.__dict__[var], var)
        return values

    def _values(self, v, o, n):
        if isinstance(o, CrawlingData):
            v[n] = o.current.values()
        elif isinstance(o, collections.Iterable) and not isinstance(o, str):
            l = []
            for i in o:
                if isinstance(i, Crawling):
                    l.append(i.values())
            v[n] = l

    def set_serial_with(self, serial):
        self._set_with('serial', serial)

    def set_timestamp_with(self, timestamp):
        self._set_with('timestamp', timestamp)

    def set_origin_with(self, origin):
        self._set_with('origin', origin)

    def _set_with(self, var, value):
        for var in self.__dict__:
            if isinstance(self.__dict__[var], CrawlingData):
                setattr(self.__dict__[var].current, var, value)

    def load(self, data):
        for var in self.__dict__:
            if isinstance(self.__dict__[var], CrawlingData):
                self.__dict__[var].set(data[var]['value'])

    def online(self, spider, context):
        self.spider = spider
        self.context = context
        if not self._persistent_loaded:
            self._load_persistent()

    def _load_persistent(self, db=None):
        self.mongo = Mongodb(conf.mongodb['host'], conf.mongodb['port'])
        self._persistent_loaded = True

    def _crawl_data(self, xpath):
        return self._crawl_data_with(self.context, xpath)

    def _crawl_data_with(self, context, xpath):
        element = self._crawl_with(context, xpath)
        if element is None:
            return None
        else:
            return element.text

    def _crawl(self, xpath):
        return self._crawl_with(self.context, xpath)

    def _crawl_with(self, context, xpath):
        element = selenium.get_by_xpath_or_none(context, xpath)
        return element

    def _crawl_link(self, xpath):
        return self._crawl_link_with(self.context, xpath)

    def _crawl_link_with(self, context, xpath):
        element = selenium.get_by_xpath(context, xpath)
        return self._get_link(context, element)

    def _crawl_all_link(self, xpath):
        return self._crawl_all_link_with(self.context, xpath)

    def _crawl_all_link_with(self, context, xpath):
        return map(lambda element: self._get_link(context, element), self._crawl_all_with(context, xpath))

    def _get_link(self, context, element):
        return context.find_element_by_link_text(element.text).get_attribute('href')

    def _crawl_all(self, xpath):
        return self._crawl_all_with(self.context, xpath)

    def _crawl_all_with(self, context, xpath):
        elements = selenium.get_all_by_xpath_or_none(context, xpath)
        return elements

    def _click(self, xpath):
        selenium.get_by_xpath(self.context, xpath).click()

    def _click_with(self, context, xpath):
        selenium.get_by_xpath(context, xpath).click()
