#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/21 0:22
# @Author  : yuchenfei
# @File    : base.py
# @Software: PyCharm
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest, wait


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # The browser intercepts the request, and does not load the
        # list page
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:invalid'
        ))

        # She starts typing some text for the new item and the error disappears
        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))

        # And she can submit it successfully
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Perversely, she now decides to submit a second blank list item
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Again, the browser will not comply
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:invalid'
        ))

        # And she can correct it by filling some text in
        self.get_item_input_box().send_keys('Make tea')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        pass
        # 用户访问首页，创建了一个清单
        self.browser.get(self.live_server_url)
        self.add_list_item('Buy wellies')

        # 不小心输入了一个重复的待办事项
        self.get_item_input_box().send_keys('Buy wellies' + Keys.ENTER)

        # 看到一条有帮助的错误消息
        self.wait_for(lambda: self.assertEqual(
            self.get_error_element().text,
            "You've already got this in your list"
        ))

    def test_error_message_are_cleared_on_input(self):
        # 新建一个清单，但方法不当，出现了一个验证错误
        self.browser.get(self.live_server_url)
        self.add_list_item('Banter too thick')
        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))

        # 为了消除错误，在输入框中输入内容
        self.get_item_input_box().send_keys('a')

        # 看到错误消息消失了
        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()
        ))
