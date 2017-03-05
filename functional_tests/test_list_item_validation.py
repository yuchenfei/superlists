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

        # 首页刷新了，显示了一个错误消息
        # 提示待办事项不能为空

        # 他输入了一些文字，然后再次提交，这次没问题了

        # 他又提交了一个空待办事项

        # 在清单页面他看到了一个类似的错误消息

        # 输入文字之后就没问题了
        self.fail('write me!')
