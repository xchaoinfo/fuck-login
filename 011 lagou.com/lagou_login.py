#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Required
- requests (必须)
Info
- author : "wuxin"
- email  : "opdss@qq.com"
- date   : "2016.4.18"

    拉勾网登录, 密码采用了md5双重加密

'''
import os
import time
import json
import sys
import subprocess
import requests
import hashlib

try:
    input = raw_input
except:
    pass

session = requests.session()

CaptchaImagePath = QRImgPath = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'captcha.jpg'

HEADERS = {
    'Referer': 'https://passport.lagou.com/login/login.html',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:44.0) Gecko/20100101 Firefox/44.0'
}

# 人工读取验证码并返回
def getCaptcha():
    captchaImgUrl = 'https://passport.lagou.com/vcode/create?from=register&refresh=%s' % time.time()
    # 写入验证码图片
    f = open(CaptchaImagePath, 'wb')
    f.write(session.get(captchaImgUrl, headers=HEADERS).content)
    f.close()
    # 打开验证码图片
    if sys.platform.find('darwin') >= 0:
        subprocess.call(['open', CaptchaImagePath])
    elif sys.platform.find('linux') >= 0:
        subprocess.call(['xdg-open', CaptchaImagePath])
    else:
        os.startfile(CaptchaImagePath)

    # 输入返回验证码
    captcha = input("请输入当前地址(% s)的验证码: " % CaptchaImagePath)
    print('你输入的验证码是:% s' % captcha)
    return captcha


# 登陆操作
def login(user, passwd, captchaData=None):
    postData = {
        'isValidate' : 'true',
        'password' : passwd,
        # 如需验证码,则添加上验证码
        'request_form_verifyCode' : (captchaData if captchaData!=None else ''),
        'submit' : '',
        'username' : user
    }
    login_url = 'https://passport.lagou.com/login/login.json'
    # data = {"content":{"rows":[]},"message":"该帐号不存在或密码错误，请重新输入","state":400}
    str = data = session.post(login_url, data=postData, headers=HEADERS).content.decode('utf-8')
    data = json.loads(data)
    if data['state'] == 1:
        return str
    elif data['state'] == 10010:
        print(data['message'])
        captchaData = getCaptcha()
        return login(user, passwd, captchaData)
    else:
        print(data['message'])
        return False


if __name__ == "__main__":
    username = input("请输入你的手机号或者邮箱\n >>>:")
    passwd = input("请输入你的密码\n >>>:")

    # 对密码进行了md5双重加密
    passwd = hashlib.md5(passwd.encode('utf-8')).hexdigest()
    # veennike 这个值是在js文件找到的一个写死的值
    passwd = 'veenike'+passwd+'veenike'
    passwd = hashlib.md5(passwd.encode('utf-8')).hexdigest()

    data = login(username, passwd)
    if data:
        print(data)
        print('登录成功')
    else:
        print('登录不成功')

