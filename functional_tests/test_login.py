#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/9/12 16:07
# @Author  : YuChenFei
# @File    : test_login.py
# @Software: PyCharm
import os
import poplib
import re
import time
from contextlib import contextmanager

from django.core import mail
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):
    # 循环中inbox.stat()获取的count不更新，故添加此辅助方法
    @contextmanager
    def pop_inbox(self):
        try:
            inbox = poplib.POP3_SSL('pop.qq.com')
            inbox.user('954833373@qq.com')
            inbox.pass_(os.environ['QQ_PASSWORD'])
            yield inbox

        finally:
            inbox.quit()

    def wait_for_email(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        start = time.time()

        while time.time() - start < 120:
            with self.pop_inbox() as inbox:
                # 获取最新的10封邮件
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print('getting msg', i)
                    _, lines, __ = inbox.retr(i)
                    lines = [l.decode('utf-8') for l in lines]
                    if f'Subject: {subject}' in lines:
                        inbox.dele(i)
                        body = '\n'.join(lines)
                        return body
            time.sleep(5)

    def test_can_get_email_link_to_log_in(self):
        # 用户进入网站主页
        # 看到导航栏有登陆区域
        # 用户输入了邮箱地址
        if self.staging_server:
            test_email = '954833373@qq.com'
        else:
            test_email = 'edith@example.com'

        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(test_email)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # 页面显示邮件已发送
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element_by_tag_name('body').text
        ))

        # 用户查看邮件找到了一条信息
        body = self.wait_for_email(test_email, SUBJECT)

        # 有一个url链接在邮件中
        self.assertIn('Use this link to log in', body)
        url_search = re.search(r'http://.+/.+$', body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # 用户点击了该链接
        self.browser.get(url)

        # 用户登录成功
        self.wait_to_be_logged_in(email=test_email)

        # 用户点击登出
        self.browser.find_element_by_link_text('Log out').click()

        # 用户成功登出
        self.wait_to_be_logged_out(email=test_email)
