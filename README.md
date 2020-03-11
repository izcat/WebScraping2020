# 武汉新冠肺炎疫情信息爬取



身处疫情中心，在家无聊写了个小程序，每天自动抓取武汉卫健委公布的武汉地区的最新具体数据。

获取网站上的公布的数据后，自动转发到我的邮箱。



共两个文件：

- main.py ：利用requests_html库，进行网站爬虫抓取疫情数据的逻辑
- mymail.py：邮箱功能的实现，将邮件从新浪邮箱转发到QQ邮箱



踩过的坑：

- session对象的`links` 和 `absolute_links` 返回的是集合set，即使转成list也是无序的

  因此从html源文件中读取到第 k 条新闻title与links[k]并不一一对应

- 解决方法：

  - [x] 使用正规式解析新闻列表元素
  - [ ] 尝试打开所有链接，检查新的页面是否是疫情信息发布页面

- 腾讯云服务器上无法运行以上代码，报错信息：ImportError: cannot import name ‘Coroutine’

  具体在 from typing import Coroutine 原因不明

- 解决方法：

  - [ ] 改用requests库