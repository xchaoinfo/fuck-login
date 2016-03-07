#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Required
- requests (必须)
Info
- author : "wuxin"
- email  : "opdss@qq.com"
- date   : "2016.3.4"

'''

import os
import re
import time
import sys
import subprocess
import requests

session = requests.session()
headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
}
#登录成功后的跳转地址
redirect_url = ''
QRImgPath = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'webQQqr.jpg'

def showQRImage():
    global QRImgPath
    url = 'https://ssl.ptlogin2.qq.com/ptqrshow'
    params = {
        'appid' : 501004106,
        'e' : 0,
        'l' : 'M',
        's' : 5,
        'd' : 72,
        'v' : 4,
        't' : time.time()
    }
    reponse = session.get(url, params=params, headers=headers)
    # print(type(reponse))  >>> <class 'requests.models.Response'>
    with open(QRImgPath, 'wb') as f :
        f.write(reponse.content)
        f.close()

    if sys.platform.find('darwin') >= 0:
        subprocess.call(['open', QRImgPath])
    elif sys.platform.find('linux') >= 0:
        subprocess.call(['xdg-open', QRImgPath])
    else:
        os.startfile(QRImgPath)

    print('请使用手机QQ扫描二维码以登录')

def waitForLogin():
    global redirect_url
    # 下面参数实在没弄明白是怎么一回事,从后面copy一个过来就能用了,以参数形式就不行,具体怎么获取的没弄明白
    url = 'https://ssl.ptlogin2.qq.com/ptqrlogin/'
    params = {
        'webqq_type' : 10,
        'remember_uin' : 1,
        'login2qq' : 1,
        'aid' : '501004106',
        'u1' : 'http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26webqq_type%3D10',
        'ptredirect' : 0,
        'ptlang' : 2052,
        'daid' : 164,
        'from_ui' : 1,
        'pttype' : 1,
        'dumy' : '',
        'fp' : 'loginerroralert',
        'action' : '0-0-8576',
        'mibao_css' : 'm_webqq',
        't' : 'undefined',
        'g' : '1',
        'js_type' : '0',
        'js_ver' : '10151',
        'login_sig' : '',
        'pt_randsalt' : '0',
    }
    #reponse = session.get(url, params=params, headers=headers)
    reponse = session.get('https://ssl.ptlogin2.qq.com/ptqrlogin?webqq_type=10&remember_uin=1&login2qq=1&aid=501004106&u1=http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26webqq_type%3D10&ptredirect=0&ptlang=2052&daid=164&from_ui=1&pttype=1&dumy=&fp=loginerroralert&action=0-0-4190&mibao_css=m_webqq&t=undefined&g=1&js_type=0&js_ver=10151&login_sig=&pt_randsalt=0', headers=headers)
    #print(reponse.url)
    content = reponse.content.decode('utf-8')
    #print(content)
    #exit()
    res = re.search(r'ptuiCB(\(.*\))\;', content).group(1)
    res = eval(res)
    '''
    # 66:未失效 65:已失效  67:二维码认证中 0:登录成功
    # 0:
    return ptuiCB('0','0','http://ptlogin4.web2.qq.com/check_sig?pttype=1&uin=479531993&service=ptqrlogin&nodirect=0&ptsigx=f89bb6133db7b0438b8f62e73e84f370b7af02c43ae56e10cbbc175efce54e822fdbd45350356f9b27ce465535ac10ad9cd2195becd7d0f6c3218f5f2e14ce34&s_url=http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26webqq_type%3D10&f_url=&ptlang=2052&ptredirect=100&aid=501004106&daid=164&j_later=0&low_login_hour=0&regmaster=0&pt_login_type=3&pt_aid=0&pt_aaid=16&pt_light=0&pt_3rd_aid=0','0','登录成功！', '阿新');
    '''
    code = res[0]
    if code == '67' :
        print('成功扫描,请在手机上确认登录')
    elif code == '0' :
        print('登录成功...')
        #取出登录成功后的跳转地址
        redirect_url = res[2]
    elif code == '65' :
        print('二维码失效,请重新启动程序')
    return code

def main():
    global redirect_url
    showQRImage()
    time.sleep(1)
    while True :
        code = waitForLogin()
        #print(code)
        if code == '0' :
            break
    os.remove(QRImgPath)
    #至此已经登录成功

    #https://ssl.ptlogin2.qq.com/ptqrshow?appid=501004106&e=0&l=M&s=5&d=72&v=4&t=0.42412856286097556
    print(redirect_url)
    reponse = session.get(redirect_url)
    print(reponse.content)

if __name__ == '__main__':
    print('开始')
    main()
    print('结束')