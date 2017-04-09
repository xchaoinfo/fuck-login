# coding: utf8

# @Author: 郭 璞
# @File: MyZhiHuLogin.py                                                                 
# @Time: 2017/4/8                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 我的模拟登录知乎

import requests
from bs4 import BeautifulSoup
import os, time
import re
# import http.cookiejar as cookielib

# 构造 Request headers
agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'
headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    'User-Agent': agent
}

######### 构造用于网络请求的session
session = requests.Session()
# session.cookies = cookielib.LWPCookieJar(filename='zhihucookie')
# try:
#     session.cookies.load(ignore_discard=True)
# except:
#     print('cookie 文件未能加载')

############ 获取xsrf_token
homeurl = 'https://www.zhihu.com'
homeresponse = session.get(url=homeurl, headers=headers)
homesoup = BeautifulSoup(homeresponse.text, 'html.parser')
xsrfinput = homesoup.find('input', {'name': '_xsrf'})
xsrf_token = xsrfinput['value']
print("获取到的xsrf_token为： ", xsrf_token)

########## 获取验证码文件
randomtime = str(int(time.time() * 1000))
captchaurl = 'https://www.zhihu.com/captcha.gif?r='+\
             randomtime+"&type=login"
captcharesponse = session.get(url=captchaurl, headers=headers)
with open('checkcode.gif', 'wb') as f:
    f.write(captcharesponse.content)
    f.close()
# os.startfile('checkcode.gif')
captcha = input('请输入验证码：')
print(captcha)

########### 开始登陆
headers['X-Xsrftoken'] = xsrf_token
headers['X-Requested-With'] = 'XMLHttpRequest'
loginurl = 'https://www.zhihu.com/login/email'
postdata = {
    '_xsrf': xsrf_token,
    'email': '邮箱@qq.com',
    'password': '密码'
}
loginresponse = session.post(url=loginurl, headers=headers, data=postdata)
print('服务器端返回响应码：', loginresponse.status_code)
print(loginresponse.json())
# 验证码问题输入导致失败: 猜测这个问题是由于session中对于验证码的请求过期导致
if loginresponse.json()['r']==1:
    # 重新输入验证码，再次运行代码则正常。也就是说可以再第一次不输入验证码，或者输入一个错误的验证码，只有第二次才是有效的
    randomtime = str(int(time.time() * 1000))
    captchaurl = 'https://www.zhihu.com/captcha.gif?r=' + \
                 randomtime + "&type=login"
    captcharesponse = session.get(url=captchaurl, headers=headers)
    with open('checkcode.gif', 'wb') as f:
        f.write(captcharesponse.content)
        f.close()
    os.startfile('checkcode.gif')
    captcha = input('请输入验证码：')
    print(captcha)

    postdata['captcha'] = captcha
    loginresponse = session.post(url=loginurl, headers=headers, data=postdata)
    print('服务器端返回响应码：', loginresponse.status_code)
    print(loginresponse.json())




##########################保存登陆后的cookie信息
# session.cookies.save()
############################判断是否登录成功
profileurl = 'https://www.zhihu.com/settings/profile'
profileresponse = session.get(url=profileurl, headers=headers)
print('profile页面响应码：', profileresponse.status_code)
profilesoup = BeautifulSoup(profileresponse.text, 'html.parser')
div = profilesoup.find('div', {'id': 'rename-section'})
print(div)
