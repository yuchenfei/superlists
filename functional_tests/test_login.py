#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/9/12 16:07
# @Author  : YuChenFei
# @File    : test_login.py
# @Software: PyCharm

from django.core import mail
from selenium.webdriver.common.keys import Keys
import re

from .base import FunctionalTest

TEST_EMAIL = 'edith@example.com'
SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):
    def test_can_get_email_link_to_log_in(self):
        # 用户进入网站主页
        # 看到导航栏有登陆区域
        # 用户输入了邮箱地址
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # 页面显示邮件已发送
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element_by_tag_name('body').text
        ))

        # 用户查看邮件找到了一条信息
        email = mail.outbox[0]  # 暂时通过邮件发送记录获取邮件
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # 有一个url链接在邮件中
        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{email.body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # 用户点击了该链接
        self.browser.get(url)

        # 用户登录成功
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Log out')
        )
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(TEST_EMAIL, navbar.text)
