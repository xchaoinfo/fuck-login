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
from BeautifulSoup import BeautifulSoup

try:
    input = raw_input
except:
    pass

#请求对象
session = requests.session()

CaptchaImagePath = QRImgPath = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'captcha.jpg'

#请求头信息
HEADERS = {
    'Referer': 'https://passport.lagou.com/login/login.html',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:51.0) Gecko/20100101 Firefox/51.0',
    # 'X-Anit-Forge-Token' : '35ed481a-e85c-45db-bf65-256546725c1c',
    #'X-Anit-Forge-Token': '636a61a6-885a-42f5-8031-bfc3c9c45073',
    # 'X-Anit-Forge-Code' : '99573313',
    #'X-Anit-Forge-Code': '99573313',
    'X-Requested-With': 'XMLHttpRequest'
}

#密码加密
def encryptPwd(passwd):
    # 对密码进行了md5双重加密
    passwd = hashlib.md5(passwd.encode('utf-8')).hexdigest()
    # veennike 这个值是在js文件找到的一个写死的值
    passwd = 'veenike'+passwd+'veenike'
    passwd = hashlib.md5(passwd.encode('utf-8')).hexdigest()
    return passwd


#获取请求token
def getTokenCode():
    login_page = 'https://passport.lagou.com/login/login.html';

    data = session.get(login_page, headers=HEADERS)

    soup = BeautifulSoup(data.content, fromEncoding='utf-8')
    '''
        页面新添加了下面这个东东, 所以要从登录页面提取token，code， 在头信息里面添加
        <!-- 页面样式 --><!-- 动态token，防御伪造请求，重复提交 -->
        <script type="text/javascript">
            window.X_Anti_Forge_Token = 'dde4db4a-888e-47ca-8277-0c6da6a8fc19';
            window.X_Anti_Forge_Code = '61142241';
        </script>
    '''
    anti_token = {'X-Anit-Forge-Token' : 'None', 'X-Anit-Forge-Code' : '0'}

    anti_token['X-Anit-Forge-Token'], anti_token['X-Anit-Forge-Code'] = map(
        lambda x:
            x.split('=')[1].strip(' ;\'')
        ,
        soup.findAll('script')[1].getText().encode('utf-8').splitlines()
    )
    return anti_token


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
def login(user, passwd, captchaData=None, token_code=None):
    postData = {
        'isValidate' : 'true',
        'password' : passwd,
        # 如需验证码,则添加上验证码
        'request_form_verifyCode' : (captchaData if captchaData!=None else ''),
        'submit' : '',
        'username' : user
    }
    login_url = 'https://passport.lagou.com/login/login.json'

    #头信息添加tokena
    login_headers = HEADERS.copy()
    token_code = getTokenCode() if token_code is None else token_code
    login_headers.update(token_code)

    # data = {"content":{"rows":[]},"message":"该帐号不存在或密码错误，请重新输入","state":400}
    response = session.post(login_url, data=postData, headers=login_headers)

    '''
    print('+++++++++++ login 请求 start +++++++++++')
    print('req.url :')
    print(response.request.url)
    print('req.headers : ')
    print(response.request.headers)
    print('req.body : ')
    print(response.request.body)
    print('res.headers : ')
    print(response.headers)
    print('res.content : ')
    print(response.content)
    print('+++++++++++ login 请求 end +++++++++++')
    '''

    data = json.loads(response.content.decode('utf-8'))

    if data['state'] == 1:
        return response.content
    elif data['state'] == 10010:
        print(data['message'])
        captchaData = getCaptcha()
        token_code = {'X-Anit-Forge-Code' : data['submitCode'], 'X-Anit-Forge-Token' : data['submitToken']}
        return login(user, passwd, captchaData, token_code)
    else:
        print(data['message'])
        return False


if __name__ == "__main__":

    username = input("请输入你的手机号或者邮箱\n >>>:")
    passwd = input("请输入你的密码\n >>>:")

    passwd = encryptPwd(passwd)

    data = login(username, passwd)
    if data:
        print(data)
        print('登录成功')
    else:
        print('登录不成功')

