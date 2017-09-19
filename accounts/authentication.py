#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/9/18 20:26
# @Author  : YuChenFei
# @File    : authentication.py
# @Software: PyCharm
from accounts.models import Token, User


class PasswordlessAuthenticationBackend(object):
    def authenticate(self, uid):
        try:
            token = Token.objects.get(uid=uid)
            return User.objects.get(email=token.email)
        except User.DoesNotExist:
            return User.objects.create(email=token.email)
        except Token.DoesNotExist:
            return None

    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
