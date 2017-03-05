#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/21 0:22
# @Author  : yuchenfei
# @File    : base.py
# @Software: PyCharm

from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # 访问首页
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # 看到输入框完美居中显示
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        # 新建了一个清单，看到输入框仍完美居中显示
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
