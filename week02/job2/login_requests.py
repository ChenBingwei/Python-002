#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用requests模拟登陆石墨文档https://shimo.im
"""

import requests
from fake_useragent import UserAgent

from common import constants
from common import exception as job2_exception

headers = constants.SHIMO_HEADERS
headers['User-Agent'] = UserAgent(verify_ssl=False).random

try:
    with requests.Session() as s:
        response = s.post(constants.SHIMO_LOGIN_URL,
                          data=constants.SHIMO_FORM_DATA,
                          headers=headers)
        print("Cookies obtained after login : {}".format(response))
except Exception as e:
    raise job2_exception.RequestsOperationError(
        "Failed to log in through the "
        "requests module: {}".format(e)
    )
