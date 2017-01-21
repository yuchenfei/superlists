#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/21 0:22
# @Author  : yuchenfei
# @File    : functional_tests.py
# @Software: PyCharm

from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrive_it_later(self):
        # 打开应用首页
        self.browser.get('http://localhost:8000')

        # 网页的标题和头部都包含“To-Do”这个词
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # 应用邀请输入一个待办事项

        # 在文本框输入“Buy peacock feathers”

        # 按下回车页面更新
        # 待办事项表格中显示了“1:Buy peacock feathers”

        # 页面中又显示了一个文本框，可以输入其他待办事项
        # 输入“Use peacock feathers to make a fly”

        # 页面再次更新，清单中显示了这两个待办事项

        # 想知道网站是否会记住这个清单
        # 网站生成了一个唯一的URL
        # 而且页面中有一些文字解说这个功能

        # 访问了这个URL，发现待办事项列表还在

        # 离开


if __name__ == '__main__':
    unittest.main()
