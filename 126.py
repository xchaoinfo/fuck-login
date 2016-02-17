#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Required
- requests (必须)
Info
- author : "xchaoinfo"
- email  : "xchaoinfo@qq.com"
- date   : "2016.2.17"

'''
import requests
import re


# 构造 Request headers
agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
headers = {
    'User-Agent': agent
}

session = requests.session()


def login(email, secret):
    session.get("http://126.com", headers=headers)
    params = {
        'df': 'mail126_letter',
        'from': 'web',
        'funcid': 'loginone',
        'iframe': '1',
        'language': '-1',
        'passtype': '1',
        'product': 'mail126',
        'verifycookie': '-1',
        'net': 'failed',
        'style': '-1',
        'race': '-2_-2_-2_db',
        'uid': email,
        'hid': '10010102'
    }
    postdata = {
        "username": email,
        "savelogin": "1",
        "url2": "http://mail.126.com/errorpage/error126.htm",
        "password": secret
    }
    url = "https://mail.126.com/entry/cgi/ntesdoor?"
    login = session.post(url, data=postdata, headers=headers, params=params)
    pa = r'href = "(.*?)"'
    res = re.findall(pa, login.text)
    index_page = session.get(res[0])
    pa_index = r"('messageCount'.*?).*?('unreadMessageCount'.*?),"
    res_index = re.findall(pa_index, index_page.text)
    print(res_index)

    return index_page

try:
    input = raw_input
except:
    pass


if __name__ == '__main__':
    email = input('请输入你的 email\n>  ')
    secret = input("请输入你的密码\n>  ")
    login(email, secret)



