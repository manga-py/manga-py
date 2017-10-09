#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
import json
import datetime
from os import path
from manga import VariablesHelper
from requests import Session
from requests.cookies import RequestsCookieJar

domainUri = 'https://www.lezhin.com'
loginUri = '/en/login/submit'

root_dir = path.dirname(path.dirname(path.realpath(__file__)))
cookies_file = path.join(root_dir, 'storage', '.lezhin_com.cookies')

def get_main_content(url, get=None, post=None):
    """
    :param url: str
    :param get: request.get
    :param post: request.post
    :return: mixed (1)
    """
    pass


def get_volumes(content=None, url=None, get=None, post=None):
    """
    :param content: mixed (1)
    :param url: str
    :return: array (2)
    """
    pass


def get_archive_name(volume, index: int = None):
    """
    :param volume: mixed (2)
    :param index: int
    :return: str
    """
    pass


def get_images(main_content=None, volume=None, get=None, post=None):
    """
    :param main_content: mixed (1)
    :param volume: mixed (2)
    :param get: request.get
    :param post: request.post
    :return: dict(str)
    """
    pass


def get_manga_name(url, get=None):
    # https://www.lezhin.com/en/comic/moonlightgarden/01
    """
    :param url: str
    :param get: request.get
    :return: str
    """
    pass


cookies = [
    VariablesHelper.user_agent,
    # {'name': None, 'value': None, 'domain': None, 'path': None}
]


def __set_cookies(session_cookies):
    global cookies
    for i in session_cookies:
        cookies.append(i)


def __refresh_cookies(url, login, password):

    session = Session()
    h = session.post(url, allow_redirects=False, data={
        'redirect': '',
        'username': login,
        'password': password,
        'remember_me': 'on',
    })

    session.close()

    return h.cookies


def __refresh_remember(remeber):
    session = Session()
    jar = RequestsCookieJar()
    jar.set(name=remeber['name'], value=remeber['value'], domain=remeber['domain'], path=remeber['path'])
    h = session.head(domainUri, allow_redirects=False, cookies=[jar])
    session.close()
    return h.cookies


def __login_helper(remeber=None):
    if not remeber:
        login = str(input('\nPlease, write you login: \n'))
        password = str(input('\nPlease, write you password: \n'))

        url = '{}{}'.format(domainUri, loginUri)
        site_cookies = __refresh_cookies(url, login, password)
    else:
        site_cookies = __refresh_remember(remeber)

    __set_cookies(site_cookies)

    return site_cookies


def _dt_now(timestamp=None):
    dt = datetime.datetime
    if isinstance(timestamp, int):
        time = dt.fromtimestamp(int(timestamp))
    elif timestamp:
        time = dt.strftime(timestamp, '')
    else:
        time = dt.now()
    return time.__format__('%y%m%d%H%M%S')


def _login():
    pass
    # if path.isfile(cookies_file):
    #     with open(cookies_file, 'r+') as c:
    #         _cookies = c.read()
    #     if not len(_cookies):
    #         c.close()
    #         with open(cookies_file, 'w+') as c:
    #             login_cookies = __login_helper()
    #         for i in login_cookies:
    #             if i.name == 'REMEMBER':
    #                 obj = {
    #                     'name': i.name,
    #                     'value': i.value,
    #                     'path': '/',
    #                     'domain': '.lezhin.com',
    #                     'expires': i.expires
    #                 }
    #                 c.write(json.dumps(obj))
    #                 c.close()
    #     else:
    #         _cookies = json.loads(_cookies)
    #         now = datetime.datetime.now()
    #         if int(_cookies['expires']) < int(now.total_seconds()):
    #             __login_helper(_cookies)
