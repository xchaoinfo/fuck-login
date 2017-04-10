# [至善网](http://www.attop.com/)模拟登录

## 前言
> 作为天朝的大学生党，大部分应该都知道至善网。
>
> 这里仅编写了模拟登录，若想进一步和至善网玩耍（你懂得）。
> 
> 可以看看我之前写的：[py-party/zz-practice](https://github.com/aloneZERO/py-party/tree/master/zz-practice)
主要涉及到 *DWRSESSIONID* 的获取、*ScriptSessionId* 的生成等等（后期会写篇博客）。

## 安装依赖
``` python
> pip install -r requirements.txt
```

## 尝试登陆
```python
# 确保已安装 Python3
> python attop.py

# 若安装 Python3 时勾选了 py launcher
# 也可执行如下命令
> py attop.py
```

## 代码文件介绍
```python
attop.py # 主程序
urls.py  # API 地址和写好的请求消息头等
```
