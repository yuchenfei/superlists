#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/9/20 16:53
# @Author  : YuChenFei
# @File    : test_my_lists.py
# @Software: PyCharm
from django.conf import settings
from django.contrib.auth import get_user_model, SESSION_KEY, BACKEND_SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore

from .base import FunctionalTest

User = get_user_model()


class MyListsTest(FunctionalTest):
    def create_pre_authenticated_session(self, email):
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        # 为了设定cookie，我们要先访问网站
        # 而404页面是加载最快的
        self.browser.get(self.server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path='/'
        ))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = 'edith@example.com'
        self.browser.get(self.server_url)
        self.wait_to_be_logged_out(email)

        # 用户已登陆
        self.create_pre_authenticated_session(email)
        self.browser.get(self.server_url)
        self.wait_to_be_logged_in(email)
