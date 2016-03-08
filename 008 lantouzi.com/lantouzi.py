#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Required
- requests (必须)
Info
- author : "wuxin"
- email  : "opdss@qq.com"
- date   : "2016.3.4"

    这个虽是个不知名的p2p网站的登录,但是采用了rsa表单加密传输处理,故写出来供大家学习参考
    如有bug, 请多多包涵

'''
import os
import time
import json
import sys
import subprocess
import base64
import requests

# 下面引入路径纯粹是因为我安装的目录的问题,
try:
    # 另外rsa 模块在python3.5 的环境现在运行会有问题,初学者,没找到问题所在,忘高手修改
    import rsa
except:
    sys.path.append('/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/site-packages')
    import rsa


try:
    input = raw_input
except:
    pass

session = requests.session()

CaptchaImagePath = QRImgPath = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'captcha.jpg'


HEADERS = {
    # 'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    # 'Accept-Encoding' : 'gzip, deflate, br',
    # 'Accept-Language' : 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Host': 'lantouzi.com',
    'Referer': 'https://lantouzi.com/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:44.0) Gecko/20100101 Firefox/44.0'
}


# 获取登陆用于加密的Key
def getPublicKey():
    login_public_key_url = 'https://lantouzi.com/api/uc/get_key?%s' % time.time()
    # 添加头信息
    headers = {'Referer': 'https://lantouzi.com/login'}
    data = session.get(login_public_key_url, headers=headers).content.decode('utf-8')
    # print(data)
    # data = "{'data': {'encrypt': {'field_name': '_encrypt_code', 'public_key': '-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDidnLFl8ivfrAtKz9YX0Qi1V4b\nq/x4lHDjswf9AQS8hzfxsbzzDaDa07V7N6PvibJYqbhrj14Pi2fGC7CED5MzQ1r6\nvwmT+wJeBC//8PVxZXo/h15g2QzfYkyp4z+IlJZYqHfYGZXu9HTsFDZhfQE8LEz3\nkbAfyb2sLcfGimQWRwIDAQAB\n-----END PUBLIC KEY-----\n', 'field_value': '480b74ab3a165ef8bf2685a0d56f6b7a'}}, 'code': 1, 'message': ''}"
    try:
        data = json.loads(data)
        if data['code'] == 1:
            return data['data']['encrypt']
        return False
    except:
        return False


# 获取验证码
def getCaptcha():
    captcha_url = 'https://lantouzi.com/captcha/access?%s' % time.time()

    headers = {'Referer': 'https://lantouzi.com/login'}
    data = session.get(captcha_url, headers=headers).content.decode('utf-8')
    # print(data)
    # data = '{"code":1,"message":"","data":{"img_url":"https:\/\/lantouzi.com\/captcha?token=576acb8684045f935242205ce33e916c","field_name":"_captcha_code","field_value":"576acb8684045f935242205ce33e916c"}}'
    data = json.loads(data)
    captcha = inputCaptcha(data['data']['img_url'], headers)
    return {
        '_captcha_code': data['data']['field_value'],
        'captcha': captcha
    }


# 人工读取验证码并返回
def inputCaptcha(captchaImgUrl, header):
    if captchaImgUrl is None or header is None:
        print('读取验证码时的参数不正确')
        return False
    # 写入验证码图片
    f = open(CaptchaImagePath, 'wb')
    f.write(session.get(captchaImgUrl, headers=header).content)
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

    encryptData = getPublicKey()

    if not encryptData:
        print(u'获取加密公钥失败')
        return False

    # user = 'pdss@qq.com'
    # passwd = '123456'

    pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(encryptData['public_key'].encode('utf-8'))

    postData = {
        '_encrypt_code': encryptData['field_value'],
        'name': base64.b64encode(rsa.encrypt(user, pubkey)),
        'password': base64.b64encode(rsa.encrypt(passwd, pubkey)),
        'verify_code': ''
    }
    # 如需验证码,则添加上验证码
    if captchaData is not None:
        postData['verify_code'] = captchaData['captcha']
        postData['_captcha_code'] = captchaData['_captcha_code']

    headers = {'Referer': 'https://lantouzi.com/login'}
    login_url = 'https://lantouzi.com/api/uc/login'
    # data = {"code":1,"message":"","data":{"id":"534287","name":"opdss","email":"opdss@qq.com","mobile":"13001928646","two_step_login_url":"https:\/\/u.dawanjia.com.cn\/user\/api\/two_step_login?token=0db3e59cb14ae35f48fae043f8669921"}}
    data = session.post(login_url, data=postData, headers=headers).content.decode('utf-8')
    print(data)
    data = json.loads(data)

    if data['code'] == 1:
        return data['data']
    elif data['code'] == -1002:
        captchaData = getCaptcha()
        # print(captchaData)
        if captchaData is not False:
            login(user, passwd, captchaData)
        else:
            print(u'验证码出错!')
            return False
    print(data['message'])
    return False


if __name__ == "__main__":
    username = input("请输入你的手机号或者邮箱\n >>>:")
    secret = input("请输入你的密码\n >>>:")
    userInfo = login(username, secret)
    print(userInfo)
    if userInfo is False:
        print('登录不成功')
        exit()

