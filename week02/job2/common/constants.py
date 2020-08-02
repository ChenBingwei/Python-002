# -*- coding: utf-8 -*-

"""
Constants used in job2
"""

SHIMO_URL = 'https://shimo.im'

# Replace the following account password
SHIMO_EMAIL = '********'
SHIMO_PASSWORD = '********'

SHIMO_FORM_DATA = {
    'email': SHIMO_EMAIL,
    'password': SHIMO_PASSWORD,
    'mobile': '+86undefined'
}

SHIMO_HEADERS = {
    'Referer': 'https://shimo.im/login?from=home',
    'authority': 'shimo.im',
    'scheme': 'https',
    'origin': 'https://shimo.im',
    'x-requested-with': 'XmlHttpRequest',
    'x-source': 'lizard-desktop',
}

SHIMO_LOGIN_URL = 'https://shimo.im/lizard-api/auth/password/login'
