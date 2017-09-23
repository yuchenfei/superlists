#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/21 0:22
# @Author  : yuchenfei
# @File    : base.py
# @Software: PyCharm
import time
import sys

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from .server_tools import reset_database

MAX_WAIT = 5


def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.staging_server = None
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.staging_server = arg.split('=')[1]
                cls.live_server_url = 'http://' + cls.staging_server
                return
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        if not cls.staging_server:
            super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Chrome()
        if self.staging_server:
            reset_database(self.staging_server)
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')

    @wait
    def wait_for(self, fn):
        return fn

    @wait
    def wait_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    @wait
    def wait_to_be_logged_in(self, email):
        self.browser.find_element_by_link_text('Log out')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        self.browser.find_element_by_name('email')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)
