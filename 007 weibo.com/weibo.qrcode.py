#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
在python2.7中测试通过
Required
- requests (必须)
- pillow (可选)
Info
- author : "fangc"
- email  : "swjfc22@163.com"
- date   : "2016.3.16"
'''
import requests
import cookielib
import time
import re
import sys

try:
    from PIL import Image
except:
    pass
import threading

# 构造 Request headers
agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'
headers = {
    'User-Agent': agent
}

session = requests.session()
session.cookies = cookielib.LWPCookieJar('weibo_cookies.txt')

# 访问 初始页面带上 cookie
index_url = "http://weibo.com/"
try:
    session.get(index_url, headers=headers, timeout=2)
except:
    session.get(index_url, headers=headers)


def open_img(image_name):
    """打开图片
    :param image_name: 图片的路径
    :return:
    """
    im = Image.open(image_name)
    im.show()
    im.close()


def login():
    """登录主函数
    :return:
    """
    image_name, qrcode_qrid = get_qrcode()
    try:
        # TODO(@fangc):用此方法打开图片不会退出，可以直接命令行用open打开，粗暴简单.
        thread = threading.Thread(target=open_img, name="open", args=(image_name,))
        thread.start()
        print(u"请用手机微博扫描二维码"
              u"微博二维码扫描在主页右上角!")
    except:
        print(u"请到当前目录下，打开二维码后用手机微博扫描二维码"
              u"微博二维码扫描在主页右上角!")
    # 下面判断是否已经扫描了二维码
    statu = 0
    while not statu:
        qrcode_check_page = scan_qrcode(qrcode_qrid, str(long(time.time() * 10000)))
        if "50114002" in qrcode_check_page:
            statu = 1
            print(u"---成功扫描，请在手机点击确认以登录---")
        time.sleep(2)

    # 下面判断是否已经点击登录,并获取alt的内容
    while statu:
        qrcode_click_page = scan_qrcode(qrcode_qrid, str(long(time.time() * 100000)))
        if "succ" in qrcode_click_page:
            # 登录成功后显示的是如下内容,需要获取到alt的内容
            # {"retcode":20000000,"msg":"succ","data":{"alt":"ALT-MTgxODQ3MTYyMQ==-sdfsfsdfsdfsfsdf-39A12129240435A0D"}}
            statu = 0
            alt = re.search(r'"alt":"(?P<alt>[\w\-\=]*)"', qrcode_click_page).group("alt")
            print(u"---登录成功---")
        time.sleep(2)

    # 下面是登录请求获取登录的跨域请求
    params = {
        "entry": "weibo",
        "returntype": "TEXT",
        "crossdomain": 1,
        "cdult": 3,
        "domain": "weibo.com",
        "alt": alt,
        "savestate": 30,
        "callback": "STK_" + str(long(time.time() * 100000))
    }
    login_url_list = "http://login.sina.com.cn/sso/login.php"
    login_list_page = session.get(login_url_list, params=params, headers=headers)
    # 返回的数据如下所示，需要提取出4个url
    # STK_145809336258600({"retcode":"0","uid":"1111111","nick":"*****@sina.cn","crossDomainUrlList":
    # ["http:***************","http:\/\***************","http:\/\/***************","http:\/\/***************"]});
    url_list = [i.replace("\/", "/") for i in login_list_page.content.split('"') if "http" in i]
    for i in url_list:
        session.get(i, headers=headers)
        time.sleep(0.5)
    session.cookies.save(ignore_discard=True, ignore_expires=True)
    print(u"欢迎你, 你在正在使用 fangc 写的模拟登录微博")


def get_qrcode():
    """获取二维码图片以及二维码编号
    :return: qrcode_image, qrcode_qrid
    """
    qrcode_before = "http://login.sina.com.cn/sso/qrcode/image?entry=weibo&size=180&callback=STK_" + str(
        long(time.time() * 10000))
    qrcode_before_page = session.get(qrcode_before, headers=headers)
    if qrcode_before_page.status_code != 200:
        sys.exit(u"可能微博改了接口!请联系作者修改")
    qrcode_before_data = qrcode_before_page.content
    qrcode_image = re.search(r'"image":"(?P<image>.*?)"', qrcode_before_data).group("image").replace("\/", "/")
    qrcode_qrid = re.search(r'"qrid":"(?P<qrid>[\w\-]*)"', qrcode_before_data).group("qrid")
    cha_page = session.get(qrcode_image, headers=headers)
    image_name = u"cha." + cha_page.headers['content-type'].split("/")[1]
    with open(image_name, 'wb') as f:
        f.write(cha_page.content)
        f.close()
    return image_name, qrcode_qrid


def scan_qrcode(qrcode_qrid, _time):
    """判断是否扫码等需要
    :param qrcode_qrid:
    :return: html
    """
    params = {
        "entry": "weibo",
        "qrid": qrcode_qrid,
        "callback": "STK_" + _time
    }
    qrcode_check = "http://login.sina.com.cn/sso/qrcode/check"
    return session.get(qrcode_check, params=params, headers=headers).content


def is_login():
    """判断是否登录成功
    :return: 登录成功返回True，失败返回False
    """
    try:
        session.cookies.load(ignore_discard=True, ignore_expires=True)
    except:
        print(u"没有检测到cookie文件")
        return False
    url = "http://weibo.com/"
    my_page = session.get(url, headers=headers)
    if "我的首页" in my_page.content:
        return True
    else:
        return False


if __name__ == '__main__':
    login()
