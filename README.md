# fuck-login

## 模拟登录一些常见的网站

主要基于以下的 Python 的第三 library 


1. [requests](http://www.python-requests.org) 处理登录
2. [pillow](https://github.com/python-pillow/Pillow) 处理验证码
3. [rsa](https://stuvel.eu/rsa) 处理加密问题

## Done

1. [知乎](http://zhihu.com)
2. [126邮箱](http://126.com)
3. [weibo.cn](http://weibo.cn) (验证码识别困难，建议不要用这种方式) 和 [mweibo.cn](http://m.weibo.cn) (推荐使用)
4. [百度](https://www.baidu.com)
5. WebQQ by [opdss](https://github.com//opdss) 还有点问题
6. Webweixin by [opdss](https://github.com//opdss)
7. [微博网页版](http://weibo.com)
8. lantouzi by [opdss](https://github.com//opdss)
9. jd.com by [henry51](https://github.com/[henry51])
10. liepin.com by [henry51](https://github.com/henry51)
11. 拉勾网 by [opdss](https://github.com//opdss)
12. xueqiu.com by xchaoinfo
13. v2ex.com by [zeekvfu](https://github.com/zeekvfu)
14. guokr.com by [Zhao Min](https://github.com/zhaozhemin)

## Todolist
0. **重构代码，增加可扩展性**
1. 增加新浪微博网页版的登录 (已解决)
2. 增加 QQ 空间 和 QQ 邮箱的登录
3. 重新组织文件结构和代码风格，make it esay to read
4. 增加可扩展性，方便添加新的功能, 现在开发新功能的例子还很不优雅。

## tips of pull request 

欢迎大家一起来 pull request 

0. pull request 尽量做到 Py2 和 Py3 版本的兼容。
1. 增加新的网站登录
2. 改进错误, Python版本的兼容
3. 基于模拟登录增加新的功能。


