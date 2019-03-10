#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .test_base import TestLinkedin
from linkedin.domain.company import Company
from linkedin.conf import company


class TestDomainCompany(TestLinkedin):
    def setup(self):
        super().setup()
        self.company = Company(None, None, company)

    def test_should_get_index(self):
        index = self.company._get_index()
        print(index)
        assert index is not None

    def test_should_find_valid_employees(self):
        employees = self.company.find_valid_employees()
        for employee in employees:
            print('%s:%s' % (employee.brief.id.get(), employee.brief.homepage.get()))
        assert len(employees) > 0
