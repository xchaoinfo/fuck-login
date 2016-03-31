# -*- coding:utf-8 -*-
'''
Required
- requests
- bs4
Info
- author : "huangfs"
- email : "huangfs@bupt.edu.cn"
- date : "2016.3.31"
'''
import requests
from bs4 import BeautifulSoup
import webbrowser

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Encoding':'gzip, deflate, sdch',
			'Accept-Language':'zh-CN,zh;q=0.8',
			'Connection':'keep-alive'
			}

session = requests.session()

def get_authcode(url):
	webbrowser.open_new_tab(url) #根据所打开网页填写验证码
	authcode = input("plz enter authcode:")
	return authcode

def get_info():
	'''获取登录相关参数'''
	try:
		login_url = "https://passport.jd.com/uc/login"
		page = session.get(login_url, headers = headers)
		soup = BeautifulSoup(page.text)
		input_list = soup.select('.form input')
		
		data = {}
		data['uuid'] = input_list[0]['value']
		data['eid'] = input_list[4]['value']
		data['fp'] = input_list[5]['value']
		data['_t'] = input_list[6]['value']
		rstr = input_list[7]['name']
		data[rstr] = input_list[7]['value']
		if soup.select('.form img') != []:
			acUrl = soup.select('.form img')[0]['src2']
			data['authcode'] = get_authcode(acUrl)
		else:
			data['authcode'] = ''
		return data
	except Exception as e:
		print (e)

def login(un, pw):
	post_url = "http://passport.jd.com/uc/loginService"
	postdata = get_info()
	postdata['loginname'] = un
	postdata['nloginpwd'] = pw
	postdata['loginpwd'] = pw
	try:
		login_page = session.post(post_url, data = postdata, headers = headers)
		#print (login_page.status_code)

		print (login_page.text)  #若返回{“success”:”http://www.jd.com”}，说明登录成功
	except Exception as e:
		print (e)

if __name__=="__main__":
	username = input("plz enter username:")
	password = input("plz enter password:")
	login(username, password)
	
