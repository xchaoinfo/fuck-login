#!python3
# coding: utf-8

# 用户中心地址
userhome_url = 'http://www.attop.com/user/index.htm'

# 登录界面地址
loginui_url = 'http://www.attop.com/login_pop.htm'

# 登录请求地址
login_url = 'http://www.attop.com/js/ajax/call/plaincall/zsClass.coreAjax.dwr'

# 登录请求参数
login_payload = {
	'callCount': 1,
	'windowName': '',
	'c0-scriptName': 'zsClass',
	'c0-methodName': 'coreAjax',
	'c0-id': 0,
	'c0-e1': 'string:{0}',  # 用户名
	'c0-e2': 'string:{0}',  # 密码
	'c0-e3': 'string:{0}',  # 验证码
	'c0-param0': 'string:loginWeb',
	'c0-e4': 'number:2',
	'c0-param1': 'Object_Object:{username:reference:c0-e1, password:reference:c0-e2, rand:reference:c0-e3, autoflag:reference:c0-e4}',
	'c0-param2': 'string:doLogin',
	'batchId': 1,
	'instanceId': 0,
	'page': '/login_pop.htm',
	'scriptSessionId': ''
}

# 登录请求消息头
login_header = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
	'Referer': 'http://www.attop.com/login_pop.htm'
}

# 验证码地址
captcha_url = 'http://www.attop.com/image.jpg'

# 通用请求消息头（模拟浏览器）
common_header = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}
