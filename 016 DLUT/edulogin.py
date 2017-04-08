# coding: utf8

# @Author: 郭 璞
# @File: DLUTEDULogin.py                                                                 
# @Time: 2017/4/8                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 大连理工大学教务处登陆
#  没有验证码,没有隐藏域，贼简单的处理

import requests
from bs4 import BeautifulSoup
import json

homeurl = 'http://zhjw.dlut.edu.cn'
loginurl = 'http://zhjw.dlut.edu.cn/loginAction.do'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Host": 'zhjw.dlut.edu.cn',
    'Referer': homeurl,
    "Upgrade-Insecure-Requests": "1",
    'loginType': 'platformLogin'
}

payload = {
    'zjh':  input('请输入账号'),
    'mm':   input('请输入密码')
}

session = requests.Session()
response = session.post(url=loginurl, headers=headers, data=payload)
print("服务器端返回状态码：", response.status_code)
# print(response.text)

# 获取当前登录用户
headers['Referer'] = 'http://zhjw.dlut.edu.cn/loginAction.do'
res = session.get(url='http://zhjw.dlut.edu.cn/menu/s_top.jsp', headers=headers)
print(res.status_code)
soup = BeautifulSoup(res.text, 'html.parser')
username = soup.find('table', {'class': "leftuser01"})
# 去除一些不必要的空格和冗余字段
username = str(username.tr.td.get_text())
#  冗余处理： ['\xa0\r\n', '', '', '', '', '', '', '', '', '', '', '', '欢迎光临\xa0 郭 璞\xa0|\xa0注销\r\n\t\t\t\r\n\t\t\t\xa0\r\n', '', '', '', '', '', '', '', '', '', '', '', '']
username = username.split(' ')[12].split('\xa0')[1]
print("当前登录用户： "+username)


