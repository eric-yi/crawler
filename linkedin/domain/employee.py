#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import linkedin.conf as conf
import linkedin.infras.utils as utils
from linkedin.domain.crawling import Crawling


class Education(Crawling):
    def __init__(self):
        super().__init__()
        self.school = self._create()
        self.degree = self._create()
        self.start_time = self._create()
        self.end_time = self._create()


class Skill(Crawling):
    def __init__(self):
        super().__init__()
        self.name = self._create()
        self.grade = self._create()
        self.category = self._create()
        self.description = self._create()


class Job(Crawling):
    def __init__(self):
        super().__init__()
        self.title = self._create()
        self.company = self._create()
        self.location = self._create()
        self.hire_time = self._create()
        self.responsibility = self._create()
        self.performance = self._create()
        self.department = self._create()


class Experience(Job):
    def __init__(self):
        super().__init__()
        self.leave_time = self._create()


class Brief(Crawling):
    def __init__(self):
        super().__init__()
        self.name = self._create()
        self.id = self._create()
        self.title = self._create()
        self.company = self._create()
        self.homepage = self._create()
        self.location = self._create()


class Profile(Job):
    def __init__(self):
        self.description = self._create()
        self.experiences = []
        self.skills = []
        self.educations = []


class Employee(Crawling):
    def __init__(self):
        self.brief = Brief()
        self.profile = Profile()
        self.index = None
        super().__init__()

    def _load_persistent(self):
        if self.index is not None:
            super()._load_persistent()
            self.mongo.set_db(self.brief.company.get())
            self.table = 'employee-information-%s' % self.index
            employee_file = os.path.join(utils.mkdir(os.path.join(conf.logs, self.brief.company.get())),
                                         self.brief.name.get())
            self.employee_store = open(employee_file, 'w')

    def set_brief(self, var, val):
        self.brief.set(var, val)

    def set_profile(self, var, val):
        self.profile.set(var, val)

    def load_brief(self, data):
        self.brief.load(data)

    def crawl(self):
        # self._click('//*[@class="pv-profile-section__see-more-inline pv-profile-section__text-truncate-toggle link"]')
        location = self._crawl_data(
            './/*[@class="pv-top-card-section__location t-16 t-black--light t-normal mt1 inline-block"]')
        self.set_brief('location', location)
        description = self._crawl_description()
        print('==== description: %s' % description)
        self.set_profile('description', description)
        experiences = self._crawl_experiences()
        self.profile.experiences = experiences
        data = {'brief': self.brief.values(), 'profile': self.profile.values()}
        self.employee_store.write(utils.to_json(data))
        self.employee_store.write('\n')
        self.employee_store.flush()
        self.mongo.insert(self.table, data)

    def _crawl_description(self):
        context = self._crawl('.//*[@class="pv-top-card-section__summary-text mt4 ember-view"]')
        lines = ['']
        if context is not None:
            for line in self._crawl_data_with(context, './/span'):
                lines.append(line)
        return ''.join(lines)

    def _crawl_experiences(self):
        context = self._crawl_all(
            './/*[@class="pv-entity__summary-info pv-entity__summary-info--background-section mb2"]')
        experiences = []
        if context is not None:
            for sub_context in context:
                experience = self._crawl_experience(sub_context)
                experiences.append(experience)
        return experiences

    def _crawl_experience(self, context):
        experience = Experience()
        company = self._crawl_data_with(context, './/*[@class="pv-entity__secondary-title"]')
        experience.set('company', company)
        title = self._crawl_data_with(context, './/*[@class="t-16 t-black t-bold"]')
        experience.set('title', title)
        location = self._crawl_experience_location(context)
        experience.set('location', location)
        time = self._crawl_experience_time(context)
        [hire_time, leave_time] = time.split('–')
        experience.set('location', location)
        experience.set('hire_time', hire_time.strip())
        experience.set('leave_time', leave_time.strip())
        print('==== hire_time: %s' % hire_time.strip())
        return experience

    def _crawl_experience_location(self, context):
        try:
            context = self._crawl_with(context, './/*[@class="pv-entity__location t-14 t-black--light t-normal block"]')
            return self._crawl_all_with(context, './/span')[1].text
        except Exception as e:
            return 'unkown'

    def _crawl_experience_time(self, context):
        context = self._crawl_with(context, './/*[@class="pv-entity__date-range t-14 t-black--light t-normal"]')
        return self._crawl_all_with(context, './/span')[1].text
