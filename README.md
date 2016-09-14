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

##Todolist
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

## something to add

0. 这个项目开始于 2016.2，有些网站改了规则，可能模拟登录不能使用了，授人以鱼不如授人以渔，后面会维护几个典型的模拟登录，并且会给出每个模拟登录的教程，初步考虑是视频，这样对于刚刚接触爬虫，对于抓包分析技术一脸懵逼的初学者来说比较友好，后面可能会更新图文的教程。教程目前制作中，我新注册了一个微信公众号 xchaoinfo, 教程的更新会在微信公众号提醒，欢迎关注

<img src="http://7xti71.com1.z0.glb.clouddn.com/xchaoinfo.jpg">

0. 项目写了一段时间后，发现代码的风格和程序的易用性，可扩展性，代码的可读性，都存在一定的问题，所以接下来最重要的是重构代码，让大家可以更容易的做出一些自己的小功能。
1. 如果你觉得某个网站的登录很有代表性，欢迎在 issue 中提出，
如果网站的登录很有意思，我会在后面的更新中加入
2. 网站的登录机制有可能经常的变动，所以当现在的模拟的登录的规则不能使用的时候，请在 issue 中提出
如果时间允许的话，我会更新。
