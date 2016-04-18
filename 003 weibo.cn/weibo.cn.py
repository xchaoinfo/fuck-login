#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Required
- requests (必须)
- pillow
Info
- author : "xchaoinfo"
- email  : "xchaoinfo@qq.com"
- date   : "2016.2.27"

考虑到 weibo.cn 变态的验证码，放弃这种浪费生命的方式吧，
2016.4.8
'''
import requests
import re
from PIL import Image


# 构造 Request headers
agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'

headers = {
    "User-Agent": agent,
    "Host": "login.weibo.cn",
    "Origin": "https://login.weibo.cn",
    "Referer": "https://login.weibo.cn/login/"
}

session = requests.session()

url_login = 'https://login.weibo.cn/login/'


def get_params(url_login):
    html = session.get(url_login, headers=headers)
    # print(html.text)
    pattern = r'action="(.*?)".*?type="password" name="(.*?)".*?name="vk" value="(.*?)".*?name="capId" value="(.*?)"'
    res = re.findall(pattern, html.text, re.S)
    # print(res)
    return res


def get_cha(capId):
    cha_url = "http://weibo.cn/interface/f/ttt/captcha/show.php?cpt="
    cha_url = cha_url + capId
    cha = session.get(cha_url, headers=headers)
    with open('cha.jpg', 'wb') as f:
        f.write(cha.content)
        f.close()
    try:
        im = Image.open('cha.jpg')
        im.show()
        im.close()
    except:
        print("请到当前目下去找cha.jpg 输入验证码")
    cha_code = input("请输入验证码")

    return cha_code



res = get_params(url_login)
if res == []:
    print("你的网络有问题，请检查网络后重试")
else:
    post_url, password, vk, capId = res[0]


if __name__ == "__main__":
    cha_code = get_cha(capId)
    email = input("请输入你的邮箱账号或者手机号码")
    password_input = input("请输入你的密码")
    postdata = {
        "mobile": email,
        "code": cha_code,
        "remember": "on",
        "backURL": "http%3A%2F%2Fweibo.cn",
        "backTitle": "手机新浪网",
        "tryCount": "",
        "vk": vk,
        "capId": capId,
        "submit": "登录",
    }
    postdata[password] = password_input
    post_url = url_login + post_url
    page = session.post(post_url, data=postdata, headers=headers)
    index = session.get("http://weibo.cn")
    print(index.text)



