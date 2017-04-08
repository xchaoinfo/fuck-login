# coding: utf8

# @Author: 郭 璞
# @File: CSDNLogin.py                                                                 
# @Time: 2017/4/7                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 模拟登陆CSDN

import re
import requests

############################################################首先获取到webflow流水号页面，来获取同一个session下的口令
url = 'https://passport.csdn.net/account/login'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
}

session = requests.session()
response = session.get(url=url, headers=headers)

lt_execution_id = re.findall('name="lt" value="(.*?)".*\sname="execution" value="(.*?)"', response.text, re.S)
payload = {
    'username': input('请输入您的账号：'),
    'password': input('请输入您的密码：'), 
    "lt": lt_execution_id[0][0],
    "execution": lt_execution_id[0][1],
    "_eventId": "submit"
}
############################################################ 此时登陆成功的话可以获取到一串JS代码，作用是可以将页面重定向到http://www.csdn.net/
response2 = session.post(url, headers=headers, data=payload)
print(response2.text)
print("*"*100)

############################################################ 对目标页面进行爬取，因为在同一个session下，所以已经是登录用户了。
response3 = session.get('http://my.csdn.net/my/score', headers=headers)
from bs4 import BeautifulSoup

soup = BeautifulSoup(response3.text, 'html.parser')
mycoin = soup.find_all('span', {'class': 'last-img'})[0]
print("当前我有了C币为："+mycoin.get_text())

################# 刷一下评论
# commenturl = 'http://blog.csdn.net/Marksinoberg/comment/submit?id=69569353'
# data = {
      # 评论人ID，也就是当前登录用户的用户名
#     'commentid':'marksinoberg',
#     'content': '赞一个',
      # 接收人ID，即被评论人的用户名
#     'replyid':'marksinoberg'
# }
# headers['Referer'] = 'http://blog.csdn.net/marksinoberg/article/details/69569353'
#
# r = session.post(url=commenturl, data=data, headers=headers)
# print("服务器端返回状态：", r.status_code)
# print("评论结果：", r.text)

################# 点赞测试
# diggurl = 'http://blog.csdn.net/marksinoberg/article/digg?ArticleId=69569353'
# diggres = session.get(url=diggurl, headers=headers)
# print("服务器端返回状态：", diggres.status_code)
# print("评论结果：", diggres.text)

################# 推送到首页（博乐才有的权限）
# publishurl = 'http://write.blog.csdn.net/bole/pub?id=69663574'
# publishres = session.get(url=publishurl, headers=headers)
# print("服务器端返回状态： ", publishres.status_code)
# print("推送结果："+publishres.text)

################ 私信测试
# 在URL中对中文进行编码处理
from urllib.parse import quote
receiver = 'marksinoberg'
body = "哈喽哈喽"
letterurl = 'http://msg.csdn.net/letters/send_message?receiver={0}&body={1}'.format(receiver, quote(body))
letterres = session.get(url=letterurl, headers=headers)
print("服务器端响应码：", letterres.status_code)
print("私信返回消息:", letterres.text)
