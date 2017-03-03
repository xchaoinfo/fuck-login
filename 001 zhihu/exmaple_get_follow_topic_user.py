#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017-02-21 19:49:57
# @Author  : xchaoinfo
# @github  : https://github.com/xchaoinfo/xchaoinfo
# @微信公众号：xchaoinfo
from bs4 import BeautifulSoup
import re
import time
import random
import http.cookiejar as cookielib
import requests

"""
1. -- 代码遵循 PEP8 规范，仅仅支持 Python3.3 及以后的版本
2. -- 当你用 login 登录获取 cookies 后，即当前文件夹下有 cookies 文件的时候
    这个例子向你展示怎么获取某个知乎某个话题所有的关注用户
"""

Topic = "https://www.zhihu.com/topic/19559205/followers"
user_agent = "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"


headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    "User-Agent": user_agent
}
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print("Cookie 未能加载")


def login_by_cookie():
    Test_login_url = "https://www.zhihu.com/settings/profile"
    login_code = session.get(Test_login_url, headers=headers, allow_redirects=False).status_code
    if login_code == 200:
        return True
    else:
        return False


def get_xsrf_followNumber(html_content):
    pattern_xsrf = r'name="_xsrf" value="(.*?)"'
    # 这里的_xsrf 返回的是一个list
    _xsrf = re.findall(pattern_xsrf, html_content)
    pa = r'\<span\>(.*?)人关注该话题'
    follow_user_num = re.findall(pa, html_content)
    # print(follow_user_num)
    # print(_xsrf)
    return _xsrf[0], follow_user_num[0]


def get_uid_pid(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    person_item = soup.find_all("div", {"class": "zm-person-item"})
    uid_list = list()
    for person in person_item:
        uid = person.find("a", {"class": "zm-list-avatar-medium"})['href']
        uid_list.append(uid)
    pid = person_item[-1]['id'].split("-")[1]

    return uid_list, pid


follow_header = {
    "Host": "www.zhihu.com",
    "Origin": "https://www.zhihu.com",
    "Referer": Topic,
    "User-Agent": user_agent,
    "X-Requested-With": "XMLHttpRequest",
    "X-Xsrftoken": "_xsrf"
}


def get_follow(_xsrf, pid, offset):
    follow_header["X-Xsrftoken"] = _xsrf
    postdata = {
        "offset": offset,
        "start": pid
    }
    html = session.post(Topic, data=postdata, headers=follow_header, timeout=3)
    if html.status_code == 200:
        content = html.json()["msg"][1]
        return get_uid_pid(content)
    else:
        return (0, 0)


def main():
    if login_by_cookie():
        print("login success")

    index_follow = session.get(Topic, headers=headers)
    html_content = index_follow.text
    _xsrf, follow_user_num = get_xsrf_followNumber(html_content)
    pages = list(range(40, int(follow_user_num), 20))[::-1]
    uid_list, pid = get_uid_pid(html_content)
    with open("user_uid.txt", 'w') as fw:
        fw.write("\n".join(uid_list))
        fw.write("\n")
        error_count = list()
        while pages:
            offset = pages.pop()
            try:
                uid_list, pid = get_follow(_xsrf, pid, offset)
                if uid_list:
                    fw.write("\n".join(uid_list))
                    fw.write("\n")
                    time.sleep(1 + random.random())
                    print(pid, offset, 'ok')
                else:
                    print(offset, 'error')
                    time.sleep(5 * random.random())
                    error_count.append(offset)
                    if error_count.count(offset) < 5:
                        pages.append(offset)
            except:
                print(offset, 'error')
                time.sleep(5 * random.random())
                error_count.append(offset)
                if error_count.count(offset) < 5:
                    pages.append(offset)


if __name__ == '__main__':
    main()
