# coding: utf8

# @Author: 郭 璞
# @File: csdn.py                                                                
# @Time: 2017/4/9                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 模拟登陆CSDN， 并实现点赞， 评论， 发私信功能

import requests
from bs4 import BeautifulSoup
#######################################################
#  Replace special characters in string using the %xx escape. Letters, digits,
#          and the characters '_.-' are never quoted.
# Python 3 可以这么引入
from urllib.parse import quote


#### 控制台输入账号密码相关, 如有特殊密码保护，应使用getpass（需要注意的是Pycharm对此支持的不好）
import getpass


# Python 2 需要这么引入
# import urllib.quote

class CSDN(object):
    """
    CSDN模拟登陆并加上点赞，评论，私信等功能。
    """
    def __init__(self, headers):
        """
        :param session: 创建全局的session对象，保证会话的一致性，有效性。
        :param headers: 防止服务器端反爬虫，添加伪装头部信息
        """
        self.session = requests.Session()
        self.headers = headers

    def login(self, account, passwd):
        """
        模拟登陆，点赞， 发评论，发私信的前提都是已在登录状态下进行的，这是前提。
        :param account: 用户名
        :param passwd:  密码
        :return:
        """

        self.username = account
        self.password = passwd

        # 只有获取到webflow流水号，才会正式进入登陆通道，服务器端对此进行了限制。
        lt, execution = self.get_webflow()
        # 要提交的表单数据
        postdata = {
            'username': account,
            'password': passwd,
            "lt": lt,
            "execution": execution,
            "_eventId": "submit"
        }

        ## 开始登陆
        loginurl = 'https://passport.csdn.net/account/login'
        response = self.session.post(url=loginurl, headers=self.headers, data=postdata)
        if response.status_code == 200:
            print('恭喜您登陆成功！')
        else:
            print(response.text)
            print('登录失败，请重试！')


    def get_webflow(self):
        """
        流水号webflow获取。随便访问包含登陆页链接的CSDN网页就可以得到这串数据。应为是动态变化的
        所以，先获取下来，以备使用。
        :return:
        """
        url = 'https://passport.csdn.net/account/login?ref=toolbar'
        response = self.session.get(url=url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        lt = soup.find('input', {'name': 'lt'})['value']
        execution = soup.find('input', {'name': 'execution'})['value']
        # 释放不必要的对象
        soup.clear()
        return (lt, execution)

    def digg(self, articleurl, digg=True):
        """
        把给定的文章路径 http://blog.csdn.net/marksinoberg/article/details/69569353
        先转化一下为： http://blog.csdn.net/marksinoberg/article/digg?ArticleId=69569353

        :param articleurl 待操作的文章路径
        :param digg: 给文章点赞还是踩一下
        :return:
        """
        try:
            bloguser, blogid = articleurl.split('/')[3], articleurl.split('/')[-1]
            if digg==True:
                diggurl = 'http://blog.csdn.net/{}/article/digg?ArticleId={}'.format(bloguser, blogid)
            else:
                diggurl = 'http://blog.csdn.net/{}/article/bury?ArticleId={}'.format(bloguser, blogid)
        except:
            print('您输入的文章路径非法！')
        print("待操作文章的路径： ", diggurl)
        self.headers['X-Requested-With'] = 'XMLHttpRequest'
        self.headers['Host'] = 'blog.csdn.net'
        self.headers['Referer'] = articleurl

        response = self.session.get(url=diggurl, headers=self.headers)
        if response.status_code == 200:
            # print("Digg 操作成功", response.text)
            articlejson = response.json()
            digg, bury = articlejson['digg'], articlejson['bury']
            print('文章：{}\n：被点赞数：{}, 被踩数：{}'.format(articleurl, digg, bury))

        else:
            print('网络或服务器出现了问题，点赞操作出现了点故障！')
        self.headers['Referer'] = ''

    def comment(self, articleurl, content):
        """
        给定一个文章的路径http://blog.csdn.net/marksinoberg/article/details/69569353，
        需要转化为形如： http://blog.csdn.net/Marksinoberg/comment/submit?id=69569353
        :param articleurl:
        :param content:
        :return:
        """
        try:
            bloguser, blogid = articleurl.split('/')[3], articleurl.split('/')[-1]
            commenturl = 'http://blog.csdn.net/{}/comment/submit?id={}'.format(bloguser, blogid)
        except:
            print(commenturl, ' 不是一个合法的路径！')
        print(commenturl)
        postdata = {
            'commentid': self.username,
            'replyid': bloguser,
            'content': content
        }
        response = self.session.post(url=commenturl, headers=self.headers, data=postdata)
        if response.status_code == 200:
            print(response.json())
            if response.json()['result'] == 1:
                print('评论成功咯！')
            else:
                print('服务器访问成功，但评论操作失败了！')
        else:
            print('评论出现了点异常！')

    def letter(self, receiver, content):
        letterurl = 'http://msg.csdn.net/letters/send_message?receiver={0}&body={1}'.format(receiver, quote(content))
        response = self.session.get(url=letterurl, headers=self.headers)
        if response.status_code == 200:
            print("私信内容发送成功！")
            # print(response.text)
            ## 这里服务器返回的是一大串HTML代码。通过解析还可以得到本人和其他博友的私信记录。
        else:
            print('私信发送失败！请检查网络是否通畅。')


    def publish_article(self):
        """
        核心URL： http://write.blog.csdn.net/postedit?edit=1&isPub=1&joinblogcontest=undefined&r=0.14573376474383326
        有兴趣的可以尝试着做一下。

        需要提交的表单信息为：
                titl:1234567                           # 博客标题
                typ:1                                  # 原创1， 转载2， 翻译3
                cont:自动发现一篇好文章的前提是什么？    #  发表的文章内容
                desc:自动发现一篇好文章的前提是什么？    # 发表的摘要信息
                tags:                                  # 标签们
                flnm:69803183                          # 博客ID（如果是新文章默认没有的）
                chnl:0                                 # 文章类型： 编程语言啊， 系统架构啊什么的
                comm:2
                level:0
                tag2:
                artid:0
                checkcode:undefined
                userinfo1:713
                stat:publish
        :return:
        """

if __name__ == '__main__':
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
    }
    csdn = CSDN(headers=headers)
    account = input('请输入您的账号：')
    password = getpass.getpass(prompt='请输入您的密码:')
    csdn.login(account=account, passwd=password)
    # 评论测试
    # csdn.comment('http://blog.csdn.net/marksinoberg/article/details/69569353', '哈哈，爬虫评论')
    # 点赞，踩测试。digg为True为顶， 为False即踩
    # csdn.digg('http://blog.csdn.net/marksinoberg/article/details/69569353', digg=True)
    # 私信测试
    # csdn.letter(receiver='marksinoberg', content='僚机呼叫主机，收到请回复，Over！')
