#!python3
# -*- coding: utf-8 -*-
"""
Info
- author : "justZero"
- email  : "alonezero@foxmail.com"
- date   : "2017-4-10"
"""

import math
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import http.cookiejar as cookielib

import urls


# 开启 session
session = requests.session()

# 模拟登录
def login(username, password):
	# 设置验证码-请求参数
	handle_captcha()

	login_payload = urls.login_payload
	# 设置用户密码-请求参数
	login_payload['c0-e1'] = login_payload['c0-e1'].format(username)
	login_payload['c0-e2'] = login_payload['c0-e2'].format(password)

	# 对请求参数进行 URL 编码
	post_data = urlencode(login_payload)

	# 开始登录
	try:
		r = session.post(
			urls.login_url,
			data = post_data,
			headers = urls.login_header
		)
		r.raise_for_status()
	except:
		print('登录失败')
		return
	else:
		# 测试模拟登录
		if test_login():
			# 保存 cookies 到文件，
			# 下次登录不需要输入账号和密码
			session.cookies.save()


# 加载本地 cookie 缓存
def load_cookie():
	session.cookies = cookielib.LWPCookieJar(filename='cookies')
	try:
		session.cookies.load(ignore_discard=True)
	except:
		print("Cookie 未能加载")


# 自动处理验证码
def handle_captcha():
	# 先打开一次登录界面，再请求验证码地址
	# 此时 cookie 中就存储了真实的验证码值
	# 幸运的是验证码值并没有被加密
	session.get(
		urls.loginui_url,
		timeout = 23,
		headers = urls.common_header
	)

	login_payload = urls.login_payload
	# 生成一个时间戳
	timestamp = str(math.floor(time.time() * 1000))
	try:
		r = session.get(
			urls.captcha_url + '?r=' + timestamp,
			timeout = 30
		)
		cookies = requests.utils.dict_from_cookiejar(session.cookies)
		r.raise_for_status()
	except:
		print('验证码处理失败')
	else:
		captcha_code = cookies['rand']
		login_payload['c0-e3'] = login_payload['c0-e3'].format(captcha_code)


# 测试模拟登录是否成功
def test_login():
	"""
	模拟登录测试
	"""
	# 测试链接（用户中心）
	test_url = urls.userhome_url
	try:
		r = session.get(test_url, timeout=23)
		r.raise_for_status()
	except:
		print('未登录\n')
		return False
	else:
		soup = BeautifulSoup(r.text, 'html.parser')
		print('=' * 100)
		# 登录成功后，访问用户中心，页面标题应是当前用户名
		# 否则页面标题含有 “登录” 字样
		title = soup.title.get_text()
		if not title.find('登录') is -1:
			print('未登录')
			print('=' * 100+'\n')
			return False
		else:
			print('登录成功\n')
			print('当前用户: ' + title.split('_')[0])
			print('=' * 100+'\n')
			return True


if __name__ == '__main__':
	load_cookie()
	if test_login():
		pass
	else:
		username = input('至善网用户名\n>  ')
		password = input('至善网密码\n>  ')
		login(username, password)
