#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用Selenium模拟登陆石墨文档https://shimo.im
"""

from selenium import webdriver

from common import constants
from common import exception as job2_exception

browser = None

try:
    """
    特殊情况说明，由于这次作业使用的调试环境为公司内网，
    网络认证与配置比较特殊，导致外部网页存在部分加载缓
    慢问题，所以设置了超时时间为20秒，并允许超时后继续
    执行以避免为了加载不需要的网页信息导致整体进程卡住。
    """
    browser = webdriver.Chrome()

    # Since the loading time of the SHIMO document
    # homepage is too long, the timeout period is
    # set to 20 seconds.
    browser.set_page_load_timeout(20)

    # It takes too long to fully load the page,
    # just load the required information.
    try:
        browser.get(constants.SHIMO_URL)
    except job2_exception.SeleniumTimeout:
        print("The complete loading page timed out, "
              "continue with subsequent operations")

    # Click the login button to enter the login page
    try:
        browser.find_element_by_xpath('//*[@id="homepage-header"]/nav/div[3]/a[2]/button').click()
    except job2_exception.SeleniumTimeout:
        print("The complete loading page timed out, "
              "continue with subsequent operations")

    # Input and login
    browser.find_element_by_xpath('//input[@type="text"]').send_keys(constants.SHIMO_EMAIL)
    browser.find_element_by_xpath('//input[@type="password"]').send_keys(constants.SHIMO_PASSWORD)
    browser.find_element_by_xpath('//button[@type="black"]').click()

    cookies = browser.get_cookies()
    print(cookies)

except Exception as e:
    raise job2_exception.SeleniumOperationError(e)

finally:
    if browser:
        browser.close()
