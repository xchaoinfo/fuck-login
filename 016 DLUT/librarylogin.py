# coding: utf8

# @Author: 郭 璞
# @File: DLUTLibraryLogin.py                                                                 
# @Time: 2017/4/7                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 大连理工大学图书馆模拟登陆，添加图片验证码处理。

import requests
from bs4 import BeautifulSoup
import os



loginurl = 'http://opac.lib.dlut.edu.cn/reader/redr_verify.php'
captchaurl = 'http://opac.lib.dlut.edu.cn/reader/captcha.php'

headers = {
    'Referer': 'http://opac.lib.dlut.edu.cn/reader/login.php',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
}

session = requests.Session()
##### 获取到验证码并保存
checkcodecontent = session.get(captchaurl, headers=headers)
with open('checkcode.gif', 'wb') as f:
    f.write(checkcodecontent.content)
print('验证码已写入到本地！')

os.startfile('checkcode.gif')
checkcode = input('请输入验证码：')
##### 准备登陆图书馆系统
payload = {
    'number':input('请输入账号：'),
    'passwd': input('请输入密码：'),
    'captcha': checkcode,
    'select':'cert_no'
}

response = session.post(loginurl, headers=headers, data=payload)
print('服务器端返回码： ', response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
## 打印当前用户
username = soup.find('font', {'color': 'blue'})
print(username.get_text())
## 打印积分信息
jifen = soup.find_all('span', {'class': 'bigger-170'})[3]
jifen = str(jifen.get_text())
print('当前登录用户总积分：', jifen)

