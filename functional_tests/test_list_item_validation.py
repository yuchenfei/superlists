#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/21 0:22
# @Author  : yuchenfei
# @File    : base.py
# @Software: PyCharm

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # 用户访问了首页，不小行提交了一个空待办事项
        # 输入框中没有输入内容，他就按下了回车键
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(' \n')

        # 首页刷新了，显示了一个错误消息
        # 提示待办事项不能为空
        error = self.get_error_element()
        self.assertEqual(error.text, "You can't have an empty list item")

        # 他输入了一些文字，然后再次提交，这次没问题了
        self.get_item_input_box().send_keys('Buy milk\n')
        self.wait_for_row_in_list_table('1: Buy milk')

        # 他又提交了一个空待办事项
        self.get_item_input_box().send_keys(' \n')

        # 在清单页面他看到了一个类似的错误消息
        self.wait_for_row_in_list_table('1: Buy milk')
        error = self.get_error_element()
        self.assertEqual(error.text, "You can't have an empty list item")

        # 输入文字之后就没问题了
        self.get_item_input_box().send_keys('Make tea\n')
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        pass
        # 用户访问首页，创建了一个清单
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Buy wellies\n')
        self.wait_for_row_in_list_table('1: Buy wellies')

        # 不小心输入了一个重复的待办事项
        self.get_item_input_box().send_keys('Buy wellies\n')

        # 看到一条有帮助的错误消息
        self.wait_for_row_in_list_table('1: Buy wellies')
        error = self.get_error_element()
        self.assertEqual(error.text, "You've already got this in your list")

    def test_error_message_are_cleared_on_input(self):
        # 新建一个清单，但方法不当，出现了一个验证错误
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(' \n')
        error = self.get_error_element()
        self.assertTrue(error.is_displayed())

        # 为了消除错误，在输入框中输入内容
        self.get_item_input_box().send_keys('a')

        # 看到错误消息消失了
        error = self.get_error_element()
        self.assertFalse(error.is_displayed())

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')
